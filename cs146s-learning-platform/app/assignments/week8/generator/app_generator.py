#!/usr/bin/env python3
"""
Week 8: AI应用生成器
使用AI辅助生成多技术栈Web应用
"""

import os
import json
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AppSpecification:
    """应用规格"""
    name: str
    description: str
    tech_stack: str
    features: List[str]
    entities: List[Dict[str, Any]]
    frontend_framework: str
    backend_framework: str
    database: str


class AppGenerator:
    """AI应用生成器"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """加载应用模板"""
        return {
            'react-flask': {
                'description': 'React前端 + Flask后端',
                'frontend': 'react',
                'backend': 'flask',
                'database': 'sqlite'
            },
            'vue-fastapi': {
                'description': 'Vue前端 + FastAPI后端',
                'frontend': 'vue',
                'backend': 'fastapi',
                'database': 'sqlite'
            },
            'angular-django': {
                'description': 'Angular前端 + Django后端',
                'frontend': 'angular',
                'backend': 'django',
                'database': 'postgresql'
            },
            'svelte-express': {
                'description': 'Svelte前端 + Express后端',
                'frontend': 'svelte',
                'backend': 'express',
                'database': 'mongodb'
            }
        }

    def generate_app(self, spec: AppSpecification, output_dir: str) -> Dict[str, Any]:
        """生成完整应用"""
        result = {
            'success': True,
            'app_path': output_dir,
            'files_generated': [],
            'warnings': [],
            'next_steps': []
        }

        try:
            # 创建应用目录结构
            self._create_directory_structure(spec, output_dir)

            # 生成后端代码
            backend_files = self._generate_backend(spec, output_dir)
            result['files_generated'].extend(backend_files)

            # 生成前端代码
            frontend_files = self._generate_frontend(spec, output_dir)
            result['files_generated'].extend(frontend_files)

            # 生成配置文件
            config_files = self._generate_config_files(spec, output_dir)
            result['files_generated'].extend(config_files)

            # 生成文档
            docs = self._generate_documentation(spec, output_dir)
            result['files_generated'].extend(docs)

            # 生成部署配置
            deployment = self._generate_deployment_config(spec, output_dir)
            result['files_generated'].extend(deployment)

            result['next_steps'] = self._get_setup_instructions(spec)

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)

        return result

    def _create_directory_structure(self, spec: AppSpecification, base_dir: str):
        """创建目录结构"""
        directories = [
            base_dir,
            f"{base_dir}/backend",
            f"{base_dir}/backend/app",
            f"{base_dir}/backend/tests",
            f"{base_dir}/frontend",
            f"{base_dir}/frontend/src",
            f"{base_dir}/frontend/public",
            f"{base_dir}/docs",
            f"{base_dir}/scripts"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _generate_backend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成后端代码"""
        files_generated = []

        if spec.backend_framework == 'flask':
            files_generated.extend(self._generate_flask_backend(spec, base_dir))
        elif spec.backend_framework == 'fastapi':
            files_generated.extend(self._generate_fastapi_backend(spec, base_dir))
        elif spec.backend_framework == 'django':
            files_generated.extend(self._generate_django_backend(spec, base_dir))
        elif spec.backend_framework == 'express':
            files_generated.extend(self._generate_express_backend(spec, base_dir))

        return files_generated

    def _generate_flask_backend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成Flask后端"""
        files = []

        # 主应用文件
        app_content = self._get_flask_app_template(spec)
        app_file = f"{base_dir}/backend/app/__init__.py"
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        files.append(app_file)

        # 模型文件
        models_content = self._get_flask_models_template(spec)
        models_file = f"{base_dir}/backend/app/models.py"
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(models_content)
        files.append(models_file)

        # 路由文件
        routes_content = self._get_flask_routes_template(spec)
        routes_file = f"{base_dir}/backend/app/routes.py"
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        files.append(routes_file)

        # 主入口文件
        main_content = self._get_flask_main_template(spec)
        main_file = f"{base_dir}/backend/run.py"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_content)
        files.append(main_file)

        # requirements.txt
        req_content = self._get_flask_requirements(spec)
        req_file = f"{base_dir}/backend/requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write(req_content)
        files.append(req_file)

        return files

    def _generate_fastapi_backend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成FastAPI后端"""
        files = []

        # 主应用文件
        app_content = self._get_fastapi_app_template(spec)
        app_file = f"{base_dir}/backend/main.py"
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        files.append(app_file)

        # 模型文件
        models_content = self._get_fastapi_models_template(spec)
        models_file = f"{base_dir}/backend/models.py"
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(models_content)
        files.append(models_file)

        # 路由文件
        routes_content = self._get_fastapi_routes_template(spec)
        routes_file = f"{base_dir}/backend/routes.py"
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        files.append(routes_file)

        # 数据库配置
        db_content = self._get_database_config(spec)
        db_file = f"{base_dir}/backend/database.py"
        with open(db_file, 'w', encoding='utf-8') as f:
            f.write(db_content)
        files.append(db_file)

        # requirements.txt
        req_content = self._get_fastapi_requirements(spec)
        req_file = f"{base_dir}/backend/requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write(req_content)
        files.append(req_file)

        return files

    def _generate_frontend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成前端代码"""
        files = []

        if spec.frontend_framework == 'react':
            files.extend(self._generate_react_frontend(spec, base_dir))
        elif spec.frontend_framework == 'vue':
            files.extend(self._generate_vue_frontend(spec, base_dir))
        elif spec.frontend_framework == 'angular':
            files.extend(self._generate_angular_frontend(spec, base_dir))
        elif spec.frontend_framework == 'svelte':
            files.extend(self._generate_svelte_frontend(spec, base_dir))

        return files

    def _generate_react_frontend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成React前端"""
        files = []

        # package.json
        package_content = self._get_react_package_json(spec)
        package_file = f"{base_dir}/frontend/package.json"
        with open(package_file, 'w', encoding='utf-8') as f:
            f.write(package_content)
        files.append(package_file)

        # 主App组件
        app_content = self._get_react_app_template(spec)
        app_file = f"{base_dir}/frontend/src/App.js"
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        files.append(app_file)

        # API服务
        api_content = self._get_react_api_service(spec)
        api_file = f"{base_dir}/frontend/src/api.js"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_content)
        files.append(api_file)

        # 组件
        for entity in spec.entities:
            component_content = self._get_react_entity_component(spec, entity)
            component_file = f"{base_dir}/frontend/src/{entity['name']}.js"
            with open(component_file, 'w', encoding='utf-8') as f:
                f.write(component_content)
            files.append(component_file)

        return files

    def _generate_vue_frontend(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成Vue前端"""
        files = []

        # package.json
        package_content = self._get_vue_package_json(spec)
        package_file = f"{base_dir}/frontend/package.json"
        with open(package_file, 'w', encoding='utf-8') as f:
            f.write(package_content)
        files.append(package_file)

        # 主App组件
        app_content = self._get_vue_app_template(spec)
        app_file = f"{base_dir}/frontend/src/App.vue"
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        files.append(app_file)

        # API服务
        api_content = self._get_vue_api_service(spec)
        api_file = f"{base_dir}/frontend/src/api.js"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_content)
        files.append(api_file)

        return files

    def _generate_config_files(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成配置文件"""
        files = []

        # Docker配置
        dockerfile_content = self._get_dockerfile(spec)
        dockerfile = f"{base_dir}/Dockerfile"
        with open(dockerfile, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        files.append(dockerfile)

        # docker-compose
        compose_content = self._get_docker_compose(spec)
        compose_file = f"{base_dir}/docker-compose.yml"
        with open(compose_file, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        files.append(compose_file)

        # 环境变量文件
        env_content = self._get_env_file(spec)
        env_file = f"{base_dir}/.env.example"
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        files.append(env_file)

        return files

    def _generate_documentation(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成文档"""
        files = []

        # README
        readme_content = self._get_readme_template(spec)
        readme_file = f"{base_dir}/README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files.append(readme_file)

        # API文档
        api_docs = self._get_api_documentation(spec)
        api_file = f"{base_dir}/docs/API.md"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_docs)
        files.append(api_file)

        return files

    def _generate_deployment_config(self, spec: AppSpecification, base_dir: str) -> List[str]:
        """生成部署配置"""
        files = []

        # 部署脚本
        deploy_content = self._get_deploy_script(spec)
        deploy_file = f"{base_dir}/scripts/deploy.sh"
        with open(deploy_file, 'w', encoding='utf-8') as f:
            f.write(deploy_content)
        files.append(deploy_file)

        return files

    def _get_setup_instructions(self, spec: AppSpecification) -> List[str]:
        """获取设置说明"""
        instructions = [
            f"cd {spec.name}",
            "后端设置:",
            f"  cd backend && pip install -r requirements.txt",
            f"  python run.py  # 或适当的启动命令",
            "",
            "前端设置:",
            f"  cd frontend && npm install",
            f"  npm run dev  # 或适当的启动命令",
            "",
            "数据库设置（如果需要）:",
            f"  创建 {spec.database} 数据库",
            f"  运行迁移脚本（如果适用）",
            "",
            "环境变量:",
            f"  复制 .env.example 到 .env",
            f"  配置数据库连接和其他设置"
        ]

        return instructions

    # 模板方法 - 这里只展示几个关键模板
    def _get_flask_app_template(self, spec: AppSpecification) -> str:
        """Flask应用模板"""
        return f'''"""
{spec.name} - Flask后端应用
{spec.description}
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .routes import register_routes

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)
    CORS(app)

    # 注册路由
    register_routes(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app
'''

    def _get_flask_models_template(self, spec: AppSpecification) -> str:
        """Flask模型模板"""
        model_code = '''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

'''

        for entity in spec.entities:
            model_code += f'''
class {entity['name'].title()}(db.Model):
    """{entity['name']} 模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {{
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }}
'''

        return model_code

    def _get_flask_routes_template(self, spec: AppSpecification) -> str:
        """Flask路由模板"""
        routes_code = '''from flask import Blueprint, request, jsonify
from .models import db

def register_routes(app):
    """注册路由"""

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'})

'''

        for entity in spec.entities:
            entity_name = entity['name'].lower()
            class_name = entity['name'].title()

            routes_code += f'''
    @app.route('/api/{entity_name}s', methods=['GET'])
    def get_{entity_name}s():
        """获取所有{entity_name}"""
        from .models import {class_name}
        items = {class_name}.query.all()
        return jsonify([item.to_dict() for item in items])

    @app.route('/api/{entity_name}s', methods=['POST'])
    def create_{entity_name}():
        """创建新{entity_name}"""
        from .models import {class_name}
        data = request.get_json()

        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400

        new_item = {class_name}(name=data['name'])
        db.session.add(new_item)
        db.session.commit()

        return jsonify(new_item.to_dict()), 201

    @app.route('/api/{entity_name}s/<int:item_id>', methods=['GET'])
    def get_{entity_name}(item_id):
        """获取特定{entity_name}"""
        from .models import {class_name}
        item = {class_name}.query.get_or_404(item_id)
        return jsonify(item.to_dict())

    @app.route('/api/{entity_name}s/<int:item_id>', methods=['PUT'])
    def update_{entity_name}(item_id):
        """更新{entity_name}"""
        from .models import {class_name}
        item = {class_name}.query.get_or_404(item_id)

        data = request.get_json()
        if 'name' in data:
            item.name = data['name']

        db.session.commit()
        return jsonify(item.to_dict())

    @app.route('/api/{entity_name}s/<int:item_id>', methods=['DELETE'])
    def delete_{entity_name}(item_id):
        """删除{entity_name}"""
        from .models import {class_name}
        item = {class_name}.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return '', 204
'''

        return routes_code

    def _get_react_app_template(self, spec: AppSpecification) -> str:
        """React App组件模板"""
        components = '\n'.join([f"import {entity['name'].title()} from './{entity['name'].title()}';" for entity in spec.entities])

        routes = '\n'.join([f'''
        <Route path="/{entity['name']}s" element={{<{entity['name'].title()} />}} />''' for entity in spec.entities])

        return f'''import React from 'react';
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom';
import './App.css';
{components}

function App() {{
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>{spec.name}</h1>
          <p>{spec.description}</p>
        </header>

        <nav>
          <ul>
            {''.join([f"<li><a href='/{entity['name']}s'>{entity['name'].title()}s</a></li>" for entity in spec.entities])}
          </ul>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={{<Home />}} />
{routes}          </Routes>
        </main>
      </div>
    </Router>
  );
}}

function Home() {{
  return <h2>Welcome to {spec.name}</h2>;
}}

export default App;
'''

    def _get_readme_template(self, spec: AppSpecification) -> str:
        """README模板"""
        return f'''# {spec.name}

{spec.description}

## 技术栈

- **前端**: {spec.frontend_framework.title()}
- **后端**: {spec.backend_framework.title()}
- **数据库**: {spec.database.title()}

## 功能特性

{chr(10).join([f"- {feature}" for feature in spec.features])}

## 快速开始

### 环境要求

- Node.js (前端)
- Python (后端)
- {spec.database} (数据库)

### 安装和运行

1. 克隆项目
```bash
git clone <repository-url>
cd {spec.name}
```

2. 后端设置
```bash
cd backend
pip install -r requirements.txt
python run.py
```

3. 前端设置
```bash
cd frontend
npm install
npm start
```

## 项目结构

```
{spec.name}/
├── backend/           # 后端代码
├── frontend/          # 前端代码
├── docs/             # 文档
├── scripts/          # 部署脚本
└── README.md         # 项目说明
```

## API文档

详见 [docs/API.md](docs/API.md)

## 部署

### 使用Docker

```bash
docker-compose up -d
```

### 手动部署

详见 [scripts/deploy.sh](scripts/deploy.sh)

## 开发

### 运行测试

```bash
# 后端测试
cd backend && python -m pytest

# 前端测试
cd frontend && npm test
```

### 代码格式化

```bash
# 后端
cd backend && black . && isort .

# 前端
cd frontend && npm run lint
```

## 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
'''

    def list_available_templates(self) -> Dict[str, Dict[str, str]]:
        """列出可用模板"""
        return self.templates

    def get_template_info(self, template_name: str) -> Optional[Dict[str, str]]:
        """获取模板信息"""
        return self.templates.get(template_name)


# 创建生成器实例
generator = AppGenerator()


def generate_app_from_prompt(prompt: str, tech_stack: str = "react-flask") -> Dict[str, Any]:
    """从自然语言提示生成应用"""
    # 简化的提示解析（实际实现会使用AI）
    spec = AppSpecification(
        name="TaskManager",
        description="任务管理系统",
        tech_stack=tech_stack,
        features=["任务创建", "任务列表", "任务状态更新"],
        entities=[
            {"name": "task", "fields": ["title", "description", "status", "due_date"]},
            {"name": "user", "fields": ["name", "email"]}
        ],
        frontend_framework=tech_stack.split('-')[0],
        backend_framework=tech_stack.split('-')[1],
        database="sqlite"
    )

    output_dir = f"generated_apps/{spec.name}_{tech_stack}"
    result = generator.generate_app(spec, output_dir)

    return result


def demonstrate_generation():
    """演示应用生成"""
    print("🚀 Week 8: AI应用生成演示")
    print("=" * 50)

    # 显示可用模板
    print("📋 可用模板:")
    templates = generator.list_available_templates()
    for name, info in templates.items():
        print(f"  - {name}: {info['description']}")

    print("
🔧 生成示例应用..."    # 生成一个示例应用
    result = generate_app_from_prompt(
        "创建一个任务管理系统，具有任务的增删改查功能",
        "react-flask"
    )

    if result['success']:
        print("✅ 应用生成成功!"        print(f"📁 生成位置: {result['app_path']}")
        print(f"📄 生成文件数: {len(result['files_generated'])}")

        print("
📋 生成的文件:"        for file in result['files_generated'][:10]:  # 只显示前10个
            print(f"  - {file}")

        if len(result['files_generated']) > 10:
            print(f"  ... 还有 {len(result['files_generated']) - 10} 个文件")

        print("
🚀 后续步骤:"        for step in result['next_steps']:
            print(f"  • {step}")
    else:
        print(f"❌ 生成失败: {result.get('error', '未知错误')}")

    print("
💡 提示:"    print("  • 每个技术栈都会生成完整的项目结构")
    print("  • 包含前后端代码、配置和文档")
    print("  • 可以直接运行和部署")
    print("  • 支持多种现代Web开发技术栈")


if __name__ == "__main__":
    demonstrate_generation()
