# FastAPI 项目入门手册（Windows 10）

> 这是本项目唯一的实操清单。每完成一项，把对应的 - [ ] 改成 - [x]。遇到错误时停在当前项，复制完整错误原文发给我；不要自行安装陌生依赖、删除目录或修改配置。

相关资料：[中文 README](README.zh-CN.md)｜[项目学习笔记](FastApi项目学习笔记.md)｜[版本化路由笔记](学习笔记-版本化路由.md)

## 使用规则

- 本地启动主线全部在 **Windows PowerShell** 执行，不要求进入 WSL。
- CMD 是传统 Windows 命令行；PowerShell 是本手册的主终端；WSL 是 Linux 环境，Docker 章节才会涉及。
- 当前电脑已确认安装 Python 3.10.11、Git、WSL 2；Docker Desktop 尚未安装。
- 当前项目没有真实数据库、没有自动入队的 RQ 业务代码，也没有测试套件。
- 不执行数据库写操作；不执行 git push；不把 .env、日志或 .venv/ 提交到 Git。

## 阶段 0：确认项目目录与 Git 状态

### 0.1 进入项目根目录

- [ ] **学习目标**：确认 PowerShell 当前就在项目根目录。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
Get-Location
Get-ChildItem
~~~

- **预期结果**：路径末尾是 external-fastapi-example，列表中有 main.py、requirements.txt、README.md。
- **失败排查**：路径不对时执行：

~~~powershell
cd 'D:\Documents\code_hub\Active_AI_Projects\Fast_Api_Demo\external-fastapi-example'
~~~

### 0.2 认识 Git 工作区

- [ ] **学习目标**：知道哪些文件会被提交，避免把本地依赖误交到 Git。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
git status --short
~~~

- **预期结果**：能看到本次学习文档或注释的修改；.venv/ 即使出现，也不要执行 git add .。
- **失败排查**：提示“不是 Git 仓库”时，回到 0.1。

## 阶段 1：检查 Python、Git 和虚拟环境

### 1.1 检查已有工具

- [ ] **学习目标**：确认 Python 与 Git 可用。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
python --version
git --version
~~~

- **预期结果**：当前电脑显示 Python 3.10.11 和 Git 版本号。
- **失败排查**：若找不到命令，先把完整报错发给我，不要同时安装多个 Python。可参考 [Python venv 官方文档](https://docs.python.org/zh-cn/3.11/library/venv.html)。

### 1.2 检查 .venv

- [ ] **学习目标**：确认依赖位于项目自己的虚拟环境，而不是全局 Python。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
Test-Path .\.venv\Scripts\python.exe
~~~

- **预期结果**：当前项目通常返回 True。
- **为什么**：.venv 是可重新创建的本地 Python 与依赖目录，不是源码。
- **失败排查**：返回 False 时继续 1.3；返回 True 时直接进入阶段 2，不要删除已有 .venv。

### 1.3 仅在 .venv 不存在时创建并安装依赖

- [ ] **学习目标**：为新克隆的项目建立本地运行环境。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

- **预期结果**：创建 .venv，并安装 FastAPI、Uvicorn、Pydantic、Redis/RQ 等依赖。
- **为什么使用完整路径**：无需激活虚拟环境，也能避开 PowerShell 的 Activate.ps1 执行策略限制。
- **失败排查**：下载超时、证书错误或“找不到 Python”时，不修改 requirements.txt；保留完整错误文本。

> 可选体验：执行 .\.venv\Scripts\Activate.ps1 可激活环境。若被执行策略拦截，继续使用完整 Python 路径即可，不必为本项目修改系统策略。

## 阶段 2：启动 FastAPI 服务

### 2.1 启动 Uvicorn

- [ ] **学习目标**：让 main.py 中的 app 成为 HTTP 服务。
- **终端**：Windows PowerShell（终端 A，保持运行）。
- **命令**：

~~~powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
~~~

- **预期结果**：出现 Uvicorn running on http://127.0.0.1:8000。
- **命令解释**：main:app 表示导入 main.py 并取得其中的 app 对象；--reload 只适合本地开发。
- **失败排查**：
  - Address already in use：8000 已被其他程序占用，先关闭已有 Uvicorn。
  - ModuleNotFoundError：回到 1.3 确认依赖已安装到 .venv。
  - 启动时 User 1 fetched...：这是单例和手动依赖注入演示，不是数据库连接。

### 2.2 查看自动接口文档

- [ ] **学习目标**：通过浏览器观察 FastAPI 自动生成的 OpenAPI 文档。
- **终端**：浏览器。
- **地址**：

~~~text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
~~~

- **预期结果**：/docs 显示 POST /api/v1/login/。
- **失败排查**：打不开时确认终端 A 仍在运行，没有导入错误。

### 2.3 停止服务

- [ ] **学习目标**：知道如何安全结束开发服务器。
- **终端**：Windows PowerShell（终端 A）。
- **操作**：按 Ctrl+C。
- **预期结果**：Uvicorn 停止，8000 端口被释放。

## 阶段 3：调用登录接口

开始前重新执行 2.1，并新开 PowerShell 终端 B。

### 3.1 在 Swagger UI 调用

- [ ] **学习目标**：先用图形界面认识请求体和响应体。
- **终端**：浏览器的 /docs。
- **操作**：展开 POST /api/v1/login/，点击 Try it out，填写：

~~~json
{
  "email": "newbie@example.com",
  "password": "123456"
}
~~~

- **预期结果**：状态码 200，响应有 access_token 与 refresh_token。
- **注意**：当前项目不校验真实用户密码；它只是 JWT 生成演示。

### 3.2 用 PowerShell 发送成功请求

- [ ] **学习目标**：不用 Swagger 也能发送 JSON HTTP 请求。
- **终端**：Windows PowerShell（终端 B）。
- **命令**：

~~~powershell
$body = @{ email = 'newbie@example.com'; password = '123456' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/v1/login/' -ContentType 'application/json' -Body $body
~~~

- **预期结果**：输出包含两个令牌属性。
- **失败排查**：连接被拒绝说明服务没启动；404 多半是地址写错，正确路径末尾带 /。

### 3.3 观察请求校验失败

- [ ] **学习目标**：确认请求校验由后端执行，不是 Swagger 替代了后端。
- **终端**：Windows PowerShell（终端 B）。
- **命令**：

~~~powershell
$badBody = @{ email = 'newbie@example.com' } | ConvertTo-Json
try {
    Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/v1/login/' -ContentType 'application/json' -Body $badBody
} catch {
    [int]$_.Exception.Response.StatusCode
}
~~~

- **预期结果**：输出 422，因为缺少必填的 password。

## 阶段 4：沿调用链读代码

- [ ] **学习目标**：读 main.py，找出 app = initApplication()、路由前缀和中间件注册。
- [ ] **学习目标**：读 routes/api.py 和 app/api/controllers/auth/login.py，解释最终 URL 为什么是 /api/v1/login/。
- [ ] **学习目标**：读 app/schemas/auth/LoginSchema.py，确认当前只要求两个字符串字段，并没有邮箱格式和密码强度规则。
- [ ] **学习目标**：读 services/AuthService.py，确认 Controller 不直接生成 JWT。
- [ ] **学习目标**：读 utils/jwt.py、settings.py、utils/timezones.py 和 utils/log.py，理解基础设施代码。
- [ ] **学习目标**：确认 loggerMiddleware.py 已注册；exampleMiddleware.py 与 dependencies/dependency.py 当前只是学习示例。

读不懂时，先查 [项目学习笔记](FastApi项目学习笔记.md) 中的“应用启动”“登录请求”“已启用、示例和未实现内容”。

## 阶段 5：配置、日志与安全边界

### 5.1 认识 .env

- [ ] **学习目标**：知道配置从哪里来，而不把密钥写进源码。
- **终端**：编辑器。
- **操作**：打开 settings.py，查看 Settings 与 env_file = ".env"。
- **预期结果**：理解 .env 可覆盖同名配置，且 .env 不应提交。
- **注意**：.env.example 当前为空。本轮只记录这个可改进点；你明确同意前不修改。

### 5.2 观察日志中间件

- [ ] **学习目标**：理解中间件如何记录请求耗时。
- **终端**：先启动服务并调用一次登录接口，再观察终端 A。
- **预期结果**：日志含状态码、请求方法、URL 和耗时；logs/ 中也会生成日志文件。

## 阶段 6：Docker、Redis 与 RQ

### 6.1 安装前检查

- [ ] **学习目标**：理解 Docker 不是本地启动的前置条件，而是后续容器化练习。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
docker version
docker compose version
~~~

- **当前预期**：本机尚未安装 Docker，会提示找不到 docker。
- **下一步**：从 [Docker Desktop Windows 官方安装页](https://docs.docker.com/desktop/setup/install/windows-install/) 下载 Docker Desktop，选择 WSL 2 backend；安装和重启由你亲自执行。
- **已知条件**：当前 Windows build 19045、WSL 2.7.11 满足基础软件版本要求；仍需确认内存和 BIOS/UEFI 虚拟化。

### 6.2 Docker 安装后的验证

- [ ] **学习目标**：确认 Docker CLI 与 Compose 可用。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
docker version
docker compose version
docker compose config
~~~

- **预期结果**：前两条显示版本，第三条能解析当前 Compose 配置。
- **失败排查**：Docker Desktop 未启动、WSL 2 backend 未启用或虚拟化未开启时，先发送完整报错。

### 6.3 启动容器并检查 Redis/Worker

- [ ] **学习目标**：观察 API、Redis、RQ Worker 如何一起运行。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
docker compose up --build
~~~

- **预期结果**：看到 app、redis、worker 日志，API 可访问 http://127.0.0.1:8000/docs。
- **停止方式**：前台按 Ctrl+C；如需移除本项目容器和网络，执行：

~~~powershell
docker compose down
~~~

- **说明**：该命令不会删除项目源码。

- [ ] **学习目标**：确认 Redis 正常，并理解 Worker 空闲属于正常状态。
- **终端**：另一个 Windows PowerShell。
- **命令**：

~~~powershell
docker compose ps
docker compose exec redis redis-cli ping
docker compose logs worker
~~~

- **预期结果**：Redis 返回 PONG；Worker 等待 default 队列。
- **说明**：当前没有 RQ 入队代码，新增最小入队示例属于后续独立练习。

## 阶段 7：测试现状

- [ ] **学习目标**：准确描述测试现状，不把手工请求成功说成 pytest 已通过。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
Get-ChildItem tests
.\.venv\Scripts\python.exe -m pip show fastapi starlette httpx httpx2
~~~

- **当前预期**：没有 tests/，并且现有环境没有 httpx、httpx2。
- **已知现象**：导入 FastAPI TestClient 时，本机 Starlette 提示缺少测试客户端依赖；FastAPI 官方教程推荐 pytest + TestClient + httpx，当前 Starlette 版本也会提到 httpx2。
- **现在不要做什么**：不要自行执行 pip install httpx 或 pip install httpx2。
- **正确下一步**：将 pip show 和导入错误发给我；我会提出最小开发依赖方案，得到你确认后再改动依赖文件。

## 阶段 8：Git 提交前固定动作

- [ ] **学习目标**：每次提交前都知道“提交了什么”。
- **终端**：Windows PowerShell。
- **命令**：

~~~powershell
git status --short
git diff
git add -- <明确的文件名>
git diff --cached --check
git diff --cached
git commit -m "📝 docs: 简短中文说明"
git log -1 --oneline
~~~

- **原则**：只显式暂存文件；不要对本项目直接使用 git add .，因为 .venv/ 尚未被忽略。
- **推送边界**：当前远程仓库是原示例仓库，未确认目标和权限前不执行 git push。

## 遇到问题时这样发给我

- [ ] 复制完整错误文本，而不只截最后一行。
- [ ] 说明正在执行哪一节、哪条命令。
- [ ] 说明是在 Windows PowerShell、CMD、WSL 还是浏览器中操作。
- [ ] 附上 python --version、git status --short 或相关命令输出。
- [ ] 在我解释原因和给出建议后，再决定是否修改代码、配置或依赖。

## 完成标志

- [ ] 我能启动 Uvicorn。
- [ ] 我能在 /docs 调用 POST /api/v1/login/。
- [ ] 我能解释 /api/v1/login/ 如何由多个路由前缀拼出来。
- [ ] 我能说清 Schema、Controller、Service、JWT 工具和日志中间件的职责。
- [ ] 我知道 Docker/RQ 当前的作用和它们尚未实现的部分。
- [ ] 我不会误把 .venv、.env 或日志提交到 Git。
