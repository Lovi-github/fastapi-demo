"""已注册的 HTTP 请求日志中间件。"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from utils.log import log
from utils.timezones import timezone_utils


class LoggerMiddleware(BaseHTTPMiddleware):
    """记录请求开始/结束时间及响应状态码。

    main.py 通过 add_middleware 注册本类，因此 Swagger、登录接口等所有 HTTP
    请求都会经过 dispatch；日志写入细节由 utils/log.py 负责。
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """将请求交给后续处理器，并在获得响应后记录耗时。"""
        start_time = timezone_utils.get_timezone_datetime()
        response = await call_next(request)
        end_time = timezone_utils.get_timezone_datetime()
        log.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
        return response
