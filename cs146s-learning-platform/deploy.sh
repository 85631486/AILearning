#!/bin/bash

# CS146S 在线学习平台部署脚本
set -e

echo "🚀 开始部署 CS146S 在线学习平台..."

# 命令存在性检查函数
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ 错误: 命令 '$1' 未找到。请确保已安装。"
        exit 1
    fi
}

# 检查必需命令
echo "🔍 检查必需命令..."
check_command python3
check_command pip
check_command gunicorn
check_command flask
check_command curl

# 检查Python版本
echo "🐍 检查Python版本..."
python3 --version

# 创建虚拟环境
echo "📦 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
echo "⬆️ 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装Python依赖..."
if [ ! -f requirements.txt ]; then
    echo "❌ 错误: requirements.txt 文件不存在"
    exit 1
fi
pip install -r requirements.txt

# 创建目录函数
create_dir() {
    local dir_path="$1"
    local dir_name="$2"
    echo "📁 创建${dir_name}目录: ${dir_path}"

    if command -v sudo &> /dev/null; then
        sudo mkdir -p "$dir_path" 2>/dev/null || {
            echo "⚠️ sudo不可用或权限不足，尝试普通用户创建..."
            mkdir -p "$dir_path" 2>/dev/null || {
                echo "⚠️ 无法创建目录: ${dir_path}，继续..."
            }
        }
        sudo chown "$USER:$USER" "$dir_path" 2>/dev/null || true
    else
        mkdir -p "$dir_path" 2>/dev/null || {
            echo "⚠️ 无法创建目录: ${dir_path}，继续..."
        }
    fi
}

# 创建必要目录
create_dir "/var/log/cs146s" "日志"
create_dir "/var/run/cs146s" "运行"
create_dir "data" "数据"
create_dir "instance" "实例"

# 环境配置
echo "⚙️ 配置环境变量..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件"
    else
        echo "❌ 错误: .env.example 文件不存在，无法创建 .env 文件"
        echo "请手动创建 .env 文件并配置以下必需变量："
        echo "  - SECRET_KEY"
        echo "  - QWEN_API_KEY (可选，用于AI功能)"
        exit 1
    fi
fi

echo "📝 请确保 .env 文件包含必要的配置:"
echo "  - SECRET_KEY: 用于Flask会话加密"
echo "  - QWEN_API_KEY: 阿里云千问API密钥（可选）"
echo "  - DATABASE_URL: 数据库连接URL（默认为SQLite）"

# 数据库初始化
echo "🗄️ 初始化数据库..."
export FLASK_APP=run.py

# 检查Flask应用是否可导入
if ! python -c "from app import create_app; print('✅ Flask应用导入成功')" 2>/dev/null; then
    echo "❌ 错误: Flask应用无法导入，请检查依赖安装"
    exit 1
fi

flask db upgrade || {
    echo "⚠️ 数据库迁移失败，可能是首次运行，继续..."
}

python data/seed_data.py || {
    echo "❌ 错误: 数据库种子数据初始化失败"
    exit 1
}

# 设置权限
echo "🔐 设置文件权限..."
chmod +x run.py 2>/dev/null || true
chmod +x deploy.sh 2>/dev/null || true

# 检查gunicorn配置
echo "🔧 检查Gunicorn配置..."
if ! python -c "import gunicorn.conf; print('✅ Gunicorn配置有效')" 2>/dev/null; then
    echo "❌ 错误: Gunicorn配置无效"
    exit 1
fi

# 启动应用
echo "⚡ 启动Flask应用..."
if gunicorn -c gunicorn.conf.py run:app --daemon; then
    echo "✅ Gunicorn服务启动成功"
else
    echo "❌ 错误: Gunicorn启动失败"
    exit 1
fi

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 健康检查
echo "🏥 运行健康检查..."
max_attempts=3
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "尝试健康检查 (${attempt}/${max_attempts})..."
    if curl -f --max-time 10 http://localhost:8000/health &>/dev/null; then
        echo "✅ 健康检查通过！"
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            echo "❌ 健康检查失败，服务可能未正确启动"
            echo "请检查日志文件: /var/log/cs146s/error.log"
            exit 1
        fi
        echo "等待重试..."
        sleep 3
        ((attempt++))
    fi
done

echo ""
echo "🎉 部署成功！"
echo "🌐 Flask应用已启动在: http://localhost:8000"
echo "🔗 API接口地址: http://localhost:8000/api/v1/"
echo ""
echo "📝 管理命令："
echo "  查看状态: sudo systemctl status cs146s (如果配置了systemd)"
echo "  重启服务: sudo systemctl restart cs146s (如果配置了systemd)"
echo "  查看日志: tail -f /var/log/cs146s/error.log"
echo "  停止服务: pkill -f gunicorn"
echo ""
echo "📋 下一步："
echo "1. 访问 http://localhost:8000 验证应用正常运行"
echo "2. 如果需要生产部署，请配置nginx反向代理"
echo "3. 设置适当的防火墙规则"
