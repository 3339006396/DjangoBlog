# 博客系统（Django REST Framework + Vue 3）

一个前后端分离的个人博客系统：后端用 Django REST Framework 提供 API，前端是 Vue 3 单页应用，支持 JWT 登录鉴权和管理后台。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端 | Django 5.2、Django REST Framework、SimpleJWT |
| 数据库 | MySQL 8 |
| 缓存 / 会话 | Redis（django-redis） |
| 跨域 | django-cors-headers |
| 前端 | Vue 3、Vite、Vue Router、Pinia、Axios |

## 功能

- 用户：邮箱验证码注册、JWT 登录、登出（Token 加入黑名单）、修改用户名 / 邮箱 / 头像
- 博客：发布、列表、我的博客、详情、删除
- 评论：发表评论
- 分类：分类列表
- 管理后台：数据统计、用户 / 博客 / 评论 / 分类管理

## 目录结构

```
DjangoProject/
├── djangoproject/        # 项目配置（settings、urls、wsgi）
├── my_auth/              # 用户模块：注册、登录、JWT、验证码、个人信息
├── blog/                 # 博客模块：博客、评论、分类
├── admin/                # 管理后台 API 模块
├── media/                # 用户上传文件（头像等，不纳入版本库）
├── frontend/             # Vue 3 前端（Vite）
└── manage.py
```

## 快速开始

### 1. 准备环境

- Python 3.13
- MySQL 8（建一个名为 `Django` 的数据库）
- Redis（本地 6379 端口）
- Node.js 18+

### 2. 后端

```bash
# 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 配置敏感信息：复制模板并填写自己的数据库密码、邮箱授权码等
copy djangoproject\local_settings.example.py djangoproject\local_settings.py

# 建表并启动
python manage.py migrate
python manage.py runserver
```

后端默认运行在 http://localhost:8000

`djangoproject/local_settings.py` 存放数据库密码、邮箱授权码、SECRET_KEY 等敏感信息，已被 `.gitignore` 忽略，不要提交到仓库。

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 http://localhost:5173 ，Vite 已配置代理，会把 `/blogs`、`/categories`、`/auth`、`/admin_api`、`/media` 请求转发到 Django（8000 端口）。

## 主要接口

| 方法 | 地址 | 说明 |
| --- | --- | --- |
| POST | `/auth/register/` | 注册 |
| POST | `/auth/login/` | 登录，返回 JWT |
| POST | `/auth/token/refresh/` | 刷新 Access Token |
| POST | `/auth/logout/` | 登出 |
| GET / PUT | `/auth/user/info/` | 获取 / 更新个人信息 |
| GET | `/auth/captcha/?email=` | 发送邮箱验证码 |
| GET | `/blogs/` | 博客列表（分页） |
| GET | `/blogs/my/` | 我的博客 |
| POST | `/blogs/create/` | 发布博客 |
| GET / DELETE | `/blogs/<id>/` | 博客详情 / 删除 |
| POST | `/blogs/<id>/comment/` | 发表评论 |
| GET | `/categories/` | 分类列表 |
| GET | `/admin/stats/` | 后台统计 |
| GET / PATCH / DELETE | `/admin/blogs/`、`/admin/comments/`、`/admin/users/`、`/admin/categories/` | 后台管理 |

除注册、登录、验证码外，接口都需要在请求头带上 `Authorization: Bearer <access_token>`。
