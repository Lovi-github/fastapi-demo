"""JWT 编码、刷新令牌创建与解码工具。

本模块只处理令牌技术细节；何时生成或刷新令牌由 AuthService 决定。
"""

from utils.timezones import timezone_utils
from datetime import datetime, timedelta
from settings import settings
from jose import jwt


async def create_access_token(sub: str, expires_delta: timedelta | None = None, **kwargs) -> tuple[str, datetime]:
    """创建访问令牌，并返回令牌字符串及其到期时间。

    sub 是 JWT 的主体（此项目中为用户 ID 字符串）；未指定有效期时使用 settings
    中的 TOKEN_EXPIRE_SECONDS。
    """
    if expires_delta:
        expire = timezone_utils.get_timezone_expire_time(expires_delta)
    else:
        expire = timezone_utils.get_timezone_expire_time(timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS))
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    
    return token, expire


async def create_refresh_token(sub: str, expire_time: datetime | None = None, **kwargs) -> tuple[str, datetime]:
    """创建刷新令牌，并返回令牌字符串及其到期时间。

    刷新令牌的消费入口尚未在当前 Router 中实现；此函数用于理解令牌分工。
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    else:
        expire = timezone_utils.get_timezone_expire_time(timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS))
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    refresh_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
   
    return refresh_token, expire

async def jwt_decode(refresh_token : str):
    """解码令牌并取回其中保存的用户 ID。

    当前示例将解码失败统一转换为异常；生产代码通常还会区分过期、签名错误和
    无效载荷，并由接口层映射为合适的 HTTP 响应。
    """
    try:
        payload = jwt.decode(refresh_token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise Exception("Token Is Not Valid")
    except :
        raise Exception("Error on Decode Token")
    return user_id

