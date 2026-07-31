# FastAPI 项目学习笔记

## 1. 这个项目在讲什么

这是一个典型的 FastAPI 后端项目：使用带版本的路由提供 API，并将接口处理、数据校验与业务逻辑分层。项目还包含 Docker、Redis 和 RQ 异步任务相关运行配置。

可以从中学习：

- FastAPI 应用如何启动、注册中间件和挂载路由。
- 通过 `http://127.0.0.1:8000/docs` 使用 FastAPI 自动生成的接口文档调试 API。
- 后端分层的职责划分。
- `.env` 与 `settings.py` 的配置管理方式，以及不要把密钥提交到 Git 的安全习惯。
- 用 Docker Compose 一次启动 API、RQ Worker 和 Redis。
- 后续可以练习新增一个小接口、补充 Pydantic 校验、为接口编写 pytest 测试。

## 2. 项目目录分层：和 Spring Boot 的对应关系

| FastAPI 位置 | Spring Boot 中常见概念 | 职责 |
| --- | --- | --- |
| `app/api/controllers/` | `@RestController` | 接收 HTTP 请求、调用业务逻辑、返回 HTTP 响应 |
| `app/schemas/` | DTO / RequestBody 类 / VO | 定义请求和响应的数据结构，并进行校验 |
| `services/` | `@Service` | 执行真正的业务逻辑，如注册、查询、计算等 |
| `routes/api.py` | 路由配置 | 组织并挂载不同接口 |

控制器应该保持轻量：它负责接收请求和返回结果；可复用的校验写在 Schema 中；真正的领域和业务逻辑写在 Service 中。

## 3. 什么是请求/响应校验

请求和响应校验不是 Apifox 一类接口工具做的事情。

- **Apifox**：外部的接口调试、测试工具。它可以帮我们发送请求、查看响应、保存接口文档。
- **Schema / DTO 校验**：后端程序自身的规则和安全边界。即使有人不用 Apifox，而是直接调用接口，后端仍然会拦住不合法的数据。

例如，注册接口要求邮箱和密码：邮箱必须是合法邮箱，密码至少 6 位。后端会在执行业务逻辑前自动检查这些规则；不符合时直接返回错误响应（FastAPI 常见为 `422`），业务代码不会继续运行。

这和 Spring Boot 中的 `@Valid`、`@RequestBody`、`@NotBlank`、`@Email`、`@Min` 等校验机制属于同一类思想。

响应校验则约束后端返回什么。例如数据库中的用户对象可能有 `password_hash`，但接口不能把它返回给前端；定义响应 Schema 后，可以只公开允许返回的字段，并确保返回格式符合接口约定。

## 4. Pydantic 是什么

`pydantic` 是 Python 的第三方数据校验库，FastAPI 经常用它来描述接口接收和返回的数据。

它主要能做两件事：

- **校验数据**：例如检查邮箱格式、密码长度、数字类型。
- **转换数据**：例如尝试将字符串 `"18"` 转换为整数 `18`。

它不是本项目自己定义的包，而是通过 `pip install` 安装的依赖。FastAPI 会借助 Pydantic 自动完成请求和响应的校验。

## 5. 读懂 Pydantic 的导入语句

```python
from pydantic import BaseModel, EmailStr, Field
```

意思是：从 `pydantic` 这个包中取出多个可用的名称。

这类似 Java 分别导入多个类：

```java
import 某个包.BaseModel;
import 某个包.EmailStr;
import 某个包.Field;
```

它们的作用并不相同：

- `BaseModel`：一个基础类，供我们定义的数据模型继承。
- `EmailStr`：一个邮箱字符串类型，用来要求字段必须符合邮箱格式。
- `Field`：一个函数，用来补充字段规则，例如最小长度。

## 6. 示例：读懂注册请求模型

下面的 `RegisterRequest` 是为了讲解 Pydantic 而写的独立示例，不是本项目当前已经存在的注册接口。本项目实际使用的是 `app/schemas/auth/LoginSchema.py` 中的 `LoginSchema`。

```python
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
```

`RegisterRequest` 是一个“注册请求的数据模型”。它规定：

- `email` 必须是符合邮箱格式的字符串。
- `password` 必须是字符串，并且至少 6 个字符。

### `class RegisterRequest(BaseModel)` 的括号是什么意思

这里的括号不是在给 `RegisterRequest` 传参数，而是在说明继承关系：`RegisterRequest` 继承 `BaseModel`。

它相当于 Java：

```java
public class RegisterRequest extends BaseModel {
}
```

继承 `BaseModel` 后，`RegisterRequest` 就拥有 Pydantic 的自动解析和校验能力。

真正创建对象、传入数据时，才会写成：

```python
request = RegisterRequest(
    email="test@example.com",
    password="123456"
)
```

这才相当于 Java 的对象创建：

```java
RegisterRequest request = new RegisterRequest(
    "test@example.com",
    "123456"
);
```

类也可以在创建对象时接收参数，本质上是在调用它的构造逻辑；但 `class RegisterRequest(BaseModel)` 中的括号用途是继承，不是构造参数。

## 7. Git：本地修改、Fork 与远程仓库

修改代码前不需要先 Fork。克隆到本地后，随时可以修改、执行 `git add` 和 `git commit`；这些提交首先只存在本机。

之后能否推送、推送到哪里，取决于远程仓库权限：

- 原仓库是自己的，或自己有写权限：可以直接 `git push` 到原仓库。
- 原仓库是别人的且没有写权限：通常先在 GitHub Fork 一份，再将本地远程指向自己的 Fork；若想把修改贡献回原项目，再发起 Pull Request（PR）。
- 只是个人实验：也可以不 Fork，在自己的 GitHub 新建空仓库后，将本地 `origin` 改为该仓库再推送。

为了既保留原项目更新来源，又能自由推送到自己的仓库，推荐这样配置：

```powershell
git remote rename origin upstream
git remote add origin https://github.com/你的用户名/你的-fork仓库.git
git push -u origin main
```

其中：

- `upstream`：原项目仓库，可用来同步上游更新。
- `origin`：自己的 Fork，可自由推送代码。

本项目当前远程仓库指向原示例仓库，且当前分支名是 `master`。在你拥有明确推送目标和权限前，只练习本地 `git add`、`git commit` 和 `git log`，不要直接执行 `git push`。

## 8. 新手应该按什么顺序学习

建议不要一上来逐个看完所有文件。按“能看到结果的最短路径”学习会更容易坚持：

1. **先跑起来**：用 Windows PowerShell 启动 Uvicorn，打开 `/docs`，亲眼看到接口文档。
2. **再发一次请求**：调用 `POST /api/v1/login/`，分别观察成功响应和 `422` 校验失败响应。
3. **沿调用链读代码**：从 `main.py` 进入路由、Controller、Schema、Service，最后到 JWT 工具。
4. **理解横切能力**：再学习配置、日志、中间件和 CORS，它们会影响所有接口。
5. **最后学习容器和异步任务**：Docker、Redis 和 RQ 是运行方式与扩展能力，不是读懂第一个接口的前置条件。
6. **再进入测试和改代码练习**：先确认测试依赖，再新增测试；不要为了练习直接修改认证逻辑。

每一步的命令、预期结果和排错方式在 [Windows 10 入门手册](FastAPI项目入门手册-Windows10.md) 中。完成一项再打勾，不需要一次全部完成。

## 9. 先认识真实目录，而不是 README 的示意结构

原英文 README 中展示的是通用模板，和当前仓库的实际位置并不完全一致。例如 `services/`、`routes/`、`utils/` 在项目根目录，而不是 `app/` 内。阅读代码时以下表为准：

| 实际位置 | 当前职责 | Spring Boot 类比 |
| --- | --- | --- |
| `main.py` | 创建 `FastAPI`，注册路由和中间件，导出 `app` | `@SpringBootApplication` + Web 配置 |
| `routes/api.py` | 汇总各 Controller 的 `APIRouter` | 统一的 `@RequestMapping` 或路由配置 |
| `app/api/controllers/` | 定义 HTTP 接口函数 | `@RestController` |
| `app/schemas/` | 描述请求数据 | DTO + `@RequestBody` |
| `services/` | 组织业务逻辑 | `@Service` |
| `utils/` | JWT、日志、时区等通用能力 | 工具类 / 基础设施组件 |
| `app/middlewares/` | 请求进入和离开接口前后的通用处理 | Filter / HandlerInterceptor |
| `settings.py` | 读取运行配置 | `application.yml` + `@ConfigurationProperties` |

## 10. 应用是怎样启动的

启动命令是：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

其中 `main:app` 的意思是：导入 `main.py` 模块，并取得其中名为 `app` 的对象。导入 `main.py` 时会执行最后一行 `app = initApplication()`，所以应用创建、路由注册、中间件注册以及当前的依赖注入演示打印都会发生在启动阶段。

```mermaid
flowchart LR
    A[Uvicorn 启动] --> B[导入 main.py]
    B --> C[执行 initApplication]
    C --> D[创建 FastAPI]
    D --> E[挂载 /api/v1 路由]
    E --> F[注册日志与 CORS 中间件]
    F --> G[导出 app]
```

`Database` 和 `UserService` 目前是理解单例与手动依赖注入的演示代码，不是真实数据库连接。启动时打印 `User 1 fetched...` 也属于这个演示的副作用。

## 11. 一次登录请求走过哪些文件

以 `POST /api/v1/login/` 为例：

```mermaid
flowchart LR
    A[客户端或 Swagger] --> B[CORS / LoggerMiddleware]
    B --> C[main.py: /api/v1]
    C --> D[routes/api.py]
    D --> E[login.py: /login/]
    E --> F[LoginSchema 校验请求体]
    F --> G[AuthService.generateTokens]
    G --> H[utils/jwt.py]
    H --> I[settings.py 和 timezones.py]
    I --> J[返回 access_token / refresh_token]
```

完整地址由三段前缀拼出来：

- `main.py`：`/api/v1`
- `login.py` 中的 Router：`/login`
- 路由函数：`/`

因此最终是 `/api/v1/login/`。这也是为什么路由前缀集中管理比在每个接口手写版本号更容易维护。更多背景见 [版本化路由专题笔记](学习笔记-版本化路由.md)。

## 12. Schema、Controller、Service 各自只做什么

`LoginSchema` 继承 `BaseModel`，当前只要求 `email` 与 `password` 两个字段存在并能解析成字符串。它**还没有**要求邮箱格式或密码长度；不要把示例中的 `EmailStr`、`Field(min_length=6)` 误认为项目现状。

- Controller `loginUser`：接收已经解析好的 `LoginSchema`，调用 Service，返回 HTTP 响应。
- Service `AuthService`：负责“生成两种令牌”这个业务动作，不应关心 URL 或 HTTP 请求对象。
- `utils/jwt.py`：负责令牌编码/解码这一通用技术细节。

这就是“Controller 薄、Service 放业务、Schema 放数据规则”的分层。以后增加真实用户校验时，应该补充 Service 和数据访问层，而不是把密码判断全部堆进 Controller。

## 13. 配置、日志、中间件与 CORS

`settings.py` 的 `Settings(BaseSettings)` 会从 `.env` 读取同名配置，并在没有配置时使用代码中的默认值。当前 `TOKEN_SECRET_KEY` 和 `secret_key` 是演示默认值，真实项目必须放在本机 `.env` 或部署平台的密钥管理中。

`LoggerMiddleware` 会记录每一次 HTTP 请求的状态码、客户端地址、方法、URL 和耗时。`utils/log.py` 会将日志写入 `logs/`，该目录已被 Git 忽略。

`CORSMiddleware` 用于浏览器跨域访问控制。这里的 `ALLOWED_HOSTS` 实际被用作 CORS 的 `allow_origins`，名称容易和“允许的 HTTP Host”混淆；本轮只记录这一点，不擅自重构配置名。

## 14. 已启用、示例和未实现的内容

| 项目部分 | 当前状态 | 学习时应如何理解 |
| --- | --- | --- |
| `LoggerMiddleware` | 已在 `main.py` 注册 | 真实请求会经过它 |
| `exampleMiddleware.py` | 未注册 | 用来了解原生 ASGI 中间件写法 |
| `dependencies/dependency.py` | 未接入路由 | 用来了解 FastAPI 的 `Depends` 前置校验写法 |
| `Database` / `UserService` | 启动时演示 | 不是实际数据库层 |
| `database/` | 空目录 | 不能认为项目已接入数据库 |
| Redis / RQ Worker | Compose 已配置 | 当前没有入队代码，Worker 等待任务正常 |

## 15. Docker、Redis 与 RQ 要学到什么

`docker-compose.yml` 定义了三个服务：

- `app`：运行 Uvicorn 的 API 容器，对外暴露 `8000` 端口。
- `redis`：提供队列和缓存可使用的 Redis 服务。
- `worker`：执行 `rq worker --url redis://redis:6379 default`，等待 `default` 队列中的任务。

本机尚未安装 Docker Desktop，所以此部分应在完成本地启动后再按手册安装和验证。不要因为看到 Worker 就误以为登录接口会自动异步执行；当前代码没有调用 RQ 入队 API。

## 16. 测试现状与正确的下一步

仓库当前没有 `tests/` 目录，不能说“测试已通过”。目前适合的验证是：编译核心模块、启动 Uvicorn、访问 OpenAPI、发送成功和失败的 HTTP 请求。

本机现有虚拟环境中，导入 `FastAPI TestClient` 时发现没有安装测试客户端依赖；当前 Starlette 会优先提示 `httpx2`，而 FastAPI 官方教程推荐 `httpx`。这不是现在自动安装依赖的理由。等你学到测试章节时，先把错误原文发给我，我会解释版本关系、给出最小开发依赖方案，得到你的确认后再改动依赖文件。

## 17. 后续练习建议

完成现有调用链后，可以按顺序练习：

1. 为登录请求增加明确的邮箱与密码规则，并观察 `422` 返回。
2. 新增一个不访问数据库的健康检查接口，练习 Router 和 Controller。
3. 为登录成功和缺少字段两种情况写 FastAPI TestClient 测试。
4. 在 Docker 环境确认 Redis 和 Worker 状态。
5. 单独设计“最小 RQ 入队任务”练习，再决定是否新增接口。

以上练习都属于后续改动：先讨论、你确认后再做，不直接改动本轮的演示登录逻辑。
