import subprocess
import tempfile
import os
import signal
import psutil
import platform
import logging
import ast
from typing import Dict, Any
from flask import current_app
from app.utils.security import CodeSecurityChecker

# Windows兼容性：signal仅在Unix系统上有效
try:
    import signal
    HAS_SIGNAL = True
except ImportError:
    HAS_SIGNAL = False

# 资源模块只在Unix系统上可用
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False

class SecureCodeExecutor:
    """安全代码执行器"""

    def __init__(self):
        self.security_checker = CodeSecurityChecker()
        # 从Flask配置中读取限制参数，提供默认值
        self.max_execution_time = self._get_config('CODE_EXECUTION_TIMEOUT', 30)
        self.max_memory_mb = self._get_config('MAX_MEMORY_MB', 100)
        self.max_cpu_time = self._get_config('MAX_CPU_TIME', 10)

    def _get_config(self, key: str, default_value: Any) -> Any:
        """从Flask配置中获取值，如果不可用则使用默认值"""
        try:
            if current_app:
                return current_app.config.get(key, default_value)
        except RuntimeError:
            # 不在应用上下文中，使用默认值
            pass
        return default_value

    def execute_code(self, code: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        安全执行Python代码

        Args:
            code: 要执行的Python代码
            inputs: 输入数据 {"stdin": "...", "args": [...]}

        Returns:
            执行结果字典
        """
        temp_file = None

        try:
            # 1. 安全检查
            security_result = self.security_checker.check_code(code)
            if not security_result['is_safe']:
                return {
                    'success': False,
                    'error': '代码包含不安全的操作',
                    'issues': security_result['issues']
                }

            # 2. 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # 3. 设置资源限制并执行
            result = self._execute_with_limits(temp_file, inputs or {})
            return result

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '代码执行超时',
                'timeout': True
            }
        except OSError as e:
            return {
                'success': False,
                'error': f'文件系统错误: {str(e)}'
            }
        except PermissionError as e:
            return {
                'success': False,
                'error': f'权限错误: {str(e)}'
            }
        except Exception as e:
            # 记录未预期的错误
            logger = logging.getLogger(__name__)
            logger.error(f'代码执行失败: {str(e)}', exc_info=True)
            return {
                'success': False,
                'error': f'执行失败: {str(e)}'
            }
        finally:
            # 4. 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except (OSError, PermissionError) as e:
                    logger = logging.getLogger(__name__)
                    logger.warning(f'清理临时文件失败 {temp_file}: {str(e)}')

    def _execute_with_limits(self, file_path: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """带资源限制的执行"""
        def set_limits():
            """设置资源限制（仅在Unix系统上）"""
            if HAS_RESOURCE:
                try:
                    # CPU时间限制
                    resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_time, self.max_cpu_time))
                    # 内存限制
                    memory_limit = self.max_memory_mb * 1024 * 1024  # 转换为字节
                    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
                except (ValueError, OSError) as e:
                    logger = logging.getLogger(__name__)
                    logger.warning(f'设置资源限制失败: {str(e)}')

        # 准备执行环境
        env = os.environ.copy()
        env['PYTHONPATH'] = ''  # 清理Python路径
        env['PYTHONDONTWRITEBYTECODE'] = '1'  # 避免生成.pyc文件

        # 使用python命令（跨平台兼容）
        python_cmd = 'python' if platform.system() == 'Windows' else 'python3'

        # 在Windows上，如果python命令不存在，尝试python3
        if platform.system() == 'Windows' and not self._command_exists(python_cmd):
            python_cmd = 'python3'
            if not self._command_exists(python_cmd):
                python_cmd = 'py'  # Windows上的Python启动器

        # 验证Python命令存在
        if not self._command_exists(python_cmd):
            raise FileNotFoundError(f"Python命令 '{python_cmd}' 未找到")

        # 执行代码
        process = subprocess.Popen(
            [python_cmd, file_path],
            stdin=subprocess.PIPE if inputs.get('stdin') else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            preexec_fn=set_limits if HAS_RESOURCE and platform.system() != 'Windows' else None,
            # Windows上不使用preexec_fn，因为它不支持
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0
        )

        try:
            # 发送输入并等待结果
            stdout, stderr = process.communicate(
                input=inputs.get('stdin', ''),
                timeout=self.max_execution_time
            )

            execution_time = self._measure_execution_time(process)

            # 检查是否超过资源限制（在不支持resource的系统上近似检查）
            if not HAS_RESOURCE and execution_time > self.max_cpu_time:
                return {
                    'success': False,
                    'stdout': stdout,
                    'stderr': stderr,
                    'returncode': process.returncode,
                    'execution_time': execution_time,
                    'error': f'执行时间超过限制 ({execution_time:.2f}s > {self.max_cpu_time}s)'
                }

            return {
                'success': process.returncode == 0,
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode,
                'execution_time': execution_time
            }

        except subprocess.TimeoutExpired:
            # 强制终止进程
            try:
                process.kill()
                # 在Unix系统上也终止进程组
                if platform.system() != 'Windows':
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except (OSError, ProcessLookupError):
                pass  # 进程可能已经终止
            raise

    def _command_exists(self, cmd: str) -> bool:
        """检查命令是否存在"""
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _measure_execution_time(self, process) -> float:
        """测量执行时间"""
        try:
            # 获取进程信息
            ps_process = psutil.Process(process.pid)
            cpu_times = ps_process.cpu_times()
            return cpu_times.user + cpu_times.system
        except:
            return 0.0
