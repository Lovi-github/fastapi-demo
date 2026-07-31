"""原生 ASGI 中间件写法示例。

本文件定义的 LoggerMiddleware 没有在 main.py 中注册，因此不会参与当前项目的
HTTP 请求。它的价值是帮助理解 BaseHTTPMiddleware 之外的 ASGI 形式。
"""

from asgiref.sync import sync_to_async
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.requests import Request


class LoggerMiddleware:
    """教学用途的原生 ASGI 中间件，不是当前启用的日志中间件。"""
    
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print ('CALL LOGGER MIDDLEWARE')
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        await self.app(scope, receive, send)
        
        return

    async def execute_request(self, request: Request, send: Send) -> None:
        """预留的教学方法，当前未被 __call__ 调用。"""
        print ('execute_request LOGGER MIDDLEWARE')
        pass

    @staticmethod
    @sync_to_async
    def exception_middleware_handler(request: Request):
        """预留的异步异常处理示例，当前未接入异常链。"""
        print ('exception_middleware_handler LOGGER MIDDLEWARE')

    @staticmethod
    @sync_to_async
    def desensitization(args: dict):
        """预留的日志脱敏示例，当前未接入请求日志处理。"""
        print ('desensitization LOGGER MIDDLEWARE')
