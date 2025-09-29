# Django Demo Application

一个基于Django的现代化Web应用，采用微服务架构，支持用户认证、异步任务处理和RESTful API。

## 🚀 技术栈

- **Web框架**: Django 5.2
- **API**: Django REST Framework
- **认证**: Django Allauth + Token认证
- **任务队列**: Celery + Redis
- **数据库**: PostgreSQL 15
- **容器化**: Docker + Docker Compose
- **缓存**: Redis 7

## ✨ 功能特性

### 🔐 用户管理
- 用户注册和登录
- Token认证
- 用户资料管理
- 邮箱验证

### 🌐 API端点
- RESTful API设计
- 用户认证API
- 异步任务API
- 任务状态查询

### ⚡ 异步任务
- Celery任务队列
- Redis作为消息代理
- 定时任务支持
- 邮件发送任务

## 🏗️ 项目架构

### 标准Django项目结构
```
pythonStudy/                   # 项目根目录
├── manage.py                  # Django管理脚本
├── pythonStudy/               # 项目配置目录
│   ├── __init__.py
│   ├── settings.py            # Django设置
│   ├── urls.py               # 主URL配置
│   ├── wsgi.py               # WSGI配置
│   └── celery.py             # Celery配置
├── api/                       # API应用
│   ├── __init__.py
│   ├── apps.py
│   ├── views.py              # API视图
│   ├── serializers.py        # 数据序列化器
│   └── urls.py               # API路由
├── tasks/                     # 任务应用
│   ├── __init__.py
│   ├── apps.py
│   └── tasks.py              # Celery任务
├── requirements.txt           # Python依赖
├── Dockerfile                # Docker镜像配置
├── docker-compose.yml        # Docker Compose配置
├── start.sh                  # 启动脚本
└── README.md                 # 项目文档
```

### 🐳 服务架构

- **web**: Django应用服务器 (端口: 8000)
- **db**: PostgreSQL数据库 (端口: 5432)
- **redis**: Redis缓存和消息队列 (端口: 6379)
- **celery**: Celery Worker处理异步任务
- **celery-beat**: Celery Beat调度定时任务

## 🚀 快速开始

### 前置要求
- Docker
- Docker Compose

### 启动应用
```bash
# 构建并启动服务
docker-compose up --build -d

# 运行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

```

4. **访问应用**
- Web应用: http://localhost:8000
- Admin后台: http://localhost:8000/admin/
- API文档: http://localhost:8000/api/

## 🛠️ 开发说明

### 本地开发
如果需要在本地开发，可以修改`.env`文件中的DEBUG设置为True，并直接运行：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python manage.py runserver
```

### 添加新任务
在`tasks/tasks.py`中添加新的Celery任务：

```python
@shared_task
def my_new_task(param1, param2):
    # 任务逻辑
    return result
```

### 添加新API端点
在`api/views.py`中添加新视图，在`api/urls.py`中配置路由。

### 数据库管理
```bash
# 创建迁移文件
docker-compose exec web python manage.py makemigrations

# 应用迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser
```

## 🔧 环境配置

### 环境变量
项目支持以下环境变量配置：

```bash
# 数据库配置
POSTGRES_DB=demo_db
POSTGRES_USER=demo_user
POSTGRES_PASSWORD=demo_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis配置
REDIS_URL=redis://redis:6379/0

# Django配置
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,web
```

## 📊 技术栈版本

- Python 3.11
- Django 5.2
- Django REST Framework 3.16
- Django Allauth 65.11
- Celery 5.5
- Redis 7
- PostgreSQL 15

## 🐳 Docker命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重新构建
docker-compose up --build -d
```