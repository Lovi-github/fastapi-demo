"""FastAPI 应用入口。

Uvicorn 通过 ``main:app`` 导入此模块。导入阶段会执行
``app = initApplication()``，因此应用、路由和中间件都在这里完成装配。
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.loggerMiddleware import LoggerMiddleware
from core.SingletonMeta import SingletonMeta


from routes.api import router

from settings import settings



class Database(metaclass=SingletonMeta):
    """单例演示用的数据库对象，并不连接真实数据库。"""

    def __init__(self):
        self.connection_string = "Database Connection Established"

    def connect(self):
        return self.connection_string


class UserService:
    """演示通过构造函数接收依赖的 Service，不是实际用户查询服务。"""

    def __init__(self, database: Database):
        self.database = database

    def get_user(self, user_id):
        # 此处仅返回演示字符串，帮助理解 Service 如何使用注入的依赖。
        return f"User {user_id} fetched using {self.database.connect()}"


def initApplication() -> FastAPI:
    """创建并装配应用。

    统一路由前缀、全局中间件和启动阶段的演示依赖都在此处配置；
    后续新增 Controller 时，应在 ``routes/api.py`` 聚合后再由这里挂载。
    """

    # 创建 ASGI 应用对象，Uvicorn 最终会对外提供它。
    fastApiApp = FastAPI()

    # 由 settings 中的 apiPrefix 和 apiVersion 统一生成 /api/v1 前缀。
    fullApiPrefix = str("/%s/%s" % (settings.apiPrefix, settings.apiVersion))
    # 将 routes/api.py 聚合的子路由挂载到统一版本前缀下。
    fastApiApp.include_router(router, prefix=fullApiPrefix)

    # 已启用的请求日志中间件；每个 HTTP 请求都会经过它。
    fastApiApp.add_middleware(LoggerMiddleware)

    # 浏览器跨域配置。中间件的注册顺序会影响请求经过它们的顺序。
    fastApiApp.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 以下三行是单例与手动依赖注入示例，当前不属于真实数据库初始化。
    db_instance = Database()
    user_service = UserService(database=db_instance)

    # 导入 main.py 时会打印演示结果；学习时不要将其理解为查询真实用户。
    print(user_service.get_user(1))

    return fastApiApp


# Uvicorn 的 ``main:app`` 中的 app 正是由这行代码导出的对象。
app = initApplication()
