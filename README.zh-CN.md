# FastAPI 示例项目（中文说明）

[English README](README.md)

这是一个用于学习 FastAPI 分层、版本化路由、Pydantic 请求模型、JWT、日志中间件和 Docker Compose 的示例项目。它适合作为“先跑起来，再沿调用链读代码”的练习仓库，而不是生产级认证系统。

## 当前项目实际具备什么

- `main.py` 创建 FastAPI 应用，挂载统一的 `/api/v1` 路由前缀，并注册日志和 CORS 中间件。
- `POST /api/v1/login/` 接收邮箱和密码字段，返回访问令牌与刷新令牌。
- `settings.py` 使用 Pydantic Settings 从 `.env` 读取配置；当前默认密钥仅用于演示，不能用于生产。
- `docker-compose.yml` 定义 API、Redis 和 RQ Worker 三个容器；当前代码没有将任务放入队列的接口，因此 Worker 空闲是正常现象。
- `database/` 目前只是目录占位，没有真实数据库连接、表结构或迁移。

## 最短启动流程（Windows PowerShell）

在项目根目录执行。若已有可用 `.venv`，不要删除它；直接从第 3 步开始即可。

```powershell
# 1. 仅在 .venv 不存在时创建虚拟环境
python -m venv .venv

# 2. 安装依赖
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. 启动开发服务器
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

启动后访问：

- Swagger UI：<http://127.0.0.1:8000/docs>
- ReDoc：<http://127.0.0.1:8000/redoc>
- OpenAPI JSON：<http://127.0.0.1:8000/openapi.json>

更完整的逐项命令、预期输出和排错方法请看 [Windows 10 入门手册](FastAPI项目入门手册-Windows10.md)。

## 真实目录结构

```text
.
├── main.py                         # Uvicorn 通过 main:app 加载的应用入口
├── settings.py                     # 环境变量与运行配置
├── routes/api.py                   # 聚合 Controller 路由
├── app/
│   ├── api/controllers/auth/login.py  # 登录接口
│   ├── schemas/auth/LoginSchema.py    # 登录请求模型
│   └── middlewares/                   # 日志与示例中间件
├── services/AuthService.py         # 令牌相关业务逻辑
├── utils/                          # JWT、日志与时区工具
├── dependencies/                   # 尚未接入路由的依赖注入示例
├── core/SingletonMeta.py           # 单例元类示例
├── database/                       # 当前为空的数据库占位目录
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 文档导航

- [FastAPI 项目学习笔记](FastApi项目学习笔记.md)：概念、架构调用链、Java/Spring Boot 对照和后续学习顺序。
- [Windows 10 入门手册](FastAPI项目入门手册-Windows10.md)：唯一的可打勾实操清单。
- [版本化路由专题笔记](学习笔记-版本化路由.md)：理解 `/api/v1` 的用途。

## 安全与学习边界

- 不要提交 `.env`、真实令牌、密码或日志文件。
- 不要把 `.venv/` 当作源码提交；本仓库当前尚未忽略它，后续会先解释风险并在你确认后再修复。
- 本项目的登录接口没有真实用户校验，令牌密钥也有演示默认值；它只用于理解代码流，不可直接上线。
- 本轮学习不执行数据库写操作，不新增数据库结构，也不自动安装 Docker 或测试依赖。
