# Django Demo Application

这是一个完整的Django培训作业演示项目，集成了以下技术栈：

- **容器化**: Docker + Docker Compose
- **Web框架**: Django 4.2
- **API**: Django REST Framework
- **权限管理**: Django Allauth
- **任务队列**: Celery + Redis
- **数据库**: PostgreSQL

## 功能特性

### 用户管理
- 用户注册和登录
- JWT Token认证
- 用户资料管理
- 邮箱验证

### API端点
- RESTful API设计
- 用户认证API
- 异步任务API
- 任务状态查询

### 异步任务
- Celery任务队列
- Redis作为消息代理
- 定时任务支持
- 邮件发送任务

## 快速开始

### 前置要求
- Docker
- Docker Compose

### 启动应用

1. 克隆项目
```bash
git clone <repository-url>
cd pythonStudy
```

2. 运行启动脚本
```bash
chmod +x start.sh
./start.sh
```

或者手动启动：
```bash
# 构建并启动服务
docker-compose up --build -d

# 运行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

# 收集静态文件
docker-compose exec web python manage.py collectstatic --noinput
```

3. 访问应用
- Web应用: http://localhost:8000
- Admin后台: http://localhost:8000/admin/
- API文档: http://localhost:8000/api/

## API使用示例

### 用户注册
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### 用户登录
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 运行异步任务
```bash
curl -X POST http://localhost:8000/api/tasks/sample/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 发送邮件
```bash
curl -X POST http://localhost:8000/api/tasks/email/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "recipient@example.com",
    "subject": "Test Email",
    "message": "This is a test message"
  }'
```

### 查询任务状态
```bash
curl http://localhost:8000/api/tasks/TASK_ID/status/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 项目结构

```
pythonStudy/
├── src/                          # Django项目源码
│   ├── demo_project/            # 主项目配置
│   │   ├── settings.py         # Django设置
│   │   ├── urls.py            # 主URL配置
│   │   ├── celery.py          # Celery配置
│   │   └── __init__.py
│   ├── api/                    # API应用
│   │   ├── views.py           # API视图
│   │   ├── serializers.py     # 数据序列化器
│   │   ├── urls.py           # API路由
│   │   └── apps.py
│   └── tasks/                 # 任务应用
│       ├── tasks.py          # Celery任务
│       └── apps.py
├── Dockerfile                 # Docker镜像配置
├── docker-compose.yml        # Docker Compose配置
├── requirements.txt          # Python依赖
├── .env                      # 环境变量
├── start.sh                  # 启动脚本
└── README.md                 # 项目文档
```

## 服务架构

- **web**: Django应用服务器
- **db**: PostgreSQL数据库
- **redis**: Redis缓存和消息队列
- **celery**: Celery Worker处理异步任务
- **celery-beat**: Celery Beat调度定时任务

## 开发说明

### 本地开发
如果需要在本地开发，可以修改`.env`文件中的DEBUG设置为True，并直接运行：

```bash
cd src
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

## 技术栈版本

- Python 3.11
- Django 4.2.7
- Django REST Framework 3.14.0
- Django Allauth 0.61.1
- Celery 5.3.4
- Redis 7
- PostgreSQL 15

## 许可证

本项目仅用于培训学习目的。
