# 仓库协作指南

## 项目结构与模块组织

`main.py` 负责创建 FastAPI 应用、注册中间件，并挂载 `routes/api.py` 中带版本的路由。HTTP 接口处理放在 `app/api/controllers/`，请求与响应模型放在 `app/schemas/`，业务逻辑放在 `services/`。通用基础能力按职责放入 `core/`、`dependencies/`、`database/` 或 `utils/`。运行配置由 `settings.py` 定义并从 `.env` 读取；不得将密钥提交到 Git。Docker 运行文件为 `Dockerfile` 和 `docker-compose.yml`（应用、RQ Worker、Redis）。

## 构建、测试与本地开发命令

- `python -m pip install -r requirements.txt`：安装项目依赖。
- `python -m uvicorn main:app --reload`：以热重载方式启动本地 API；可访问 `http://127.0.0.1:8000/docs` 调试接口。
- `docker compose up --build`：构建并启动 API、RQ Worker 和 Redis。
- `python -m pytest`：在补充测试后运行完整测试套件。

## 编码风格与命名规范

使用四空格缩进；公共接口应提供类型标注；不直观的逻辑应写简短文档字符串。新增 Python 代码遵循：模块、函数和变量使用 `snake_case`，类使用 `PascalCase`，常量使用 `UPPER_CASE`。`AuthService.py`、`loggerMiddleware.py` 等既有文件已被直接导入，避免顺手重命名。控制器应保持轻量；通用校验放入 Pydantic Schema，领域逻辑放入 Service。

## 测试规范

当前仓库尚未提交测试套件。新增测试请放在 `tests/`，文件命名为 `test_<module>.py`，函数命名为 `test_<behavior>`，例如 `tests/test_login.py`。修改接口时应覆盖成功与失败响应；适用时优先使用 FastAPI TestClient，不依赖真实运行的服务。所有任务完成后再统一运行完整测试。

## 数据库、配置与安全

未经明确授权，不得执行数据库写操作或修改表结构。获批的表结构或数据迁移必须同时新增 `database/migration/` 下幂等的增量 SQL，并更新初始化建表脚本。不得提交 `.env`、凭据、令牌或生成的日志文件。

## 提交与拉取请求规范

现有历史多为简短的功能描述；新提交统一使用 `<emoji> <type>: <简短描述>`，例如 `🐛 fix: 校验刷新令牌`。可用类型：`💥feat`、`🐛fix`、`📝docs`、`🎨style`、`♻️refactor`、`⚡perf`、`🥑test`、`🔧chore`、`🚀deploy`。每个 PR 应聚焦单一主题，说明行为变化和验证方式，关联 Issue；接口可见的改动需附请求/响应示例或截图。功能完成后先等待用户测试确认，再创建正式提交。
