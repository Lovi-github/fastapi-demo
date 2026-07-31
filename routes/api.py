"""项目级路由聚合点。

Controller 只声明自身业务前缀；这里负责把它们组合成一个总 Router，
最终再由 main.py 统一加上 API 版本前缀。
"""

from fastapi import APIRouter

from app.api.controllers.auth.login import router as login_api

router = APIRouter()


def includeApiRoutes():
    """将各业务 Router 挂到总 Router。

    版本前缀不在这里重复书写，而是在 main.py 的 include_router 中统一添加。
    """
    router.include_router(login_api)


includeApiRoutes()
