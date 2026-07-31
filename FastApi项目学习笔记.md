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

## 6. 读懂注册请求模型

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

