"""认证相关的业务编排层。"""

from utils.jwt import create_access_token, create_refresh_token, jwt_decode
from datetime import datetime


class AuthService:
    @staticmethod
    async def generateTokens(user_id: int) -> dict:
        """为指定用户标识生成访问令牌和刷新令牌。

        Controller 只调用这个方法；具体 JWT 编码细节继续下沉到 utils/jwt.py。
        """

        access_token, _ = await create_access_token(
            str(user_id), multi_login=False
        )

        refresh_token, _ = await create_refresh_token(
            str(user_id), multi_login=False
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    async def generateNewAccessToken(*, refresh_token: str) -> tuple[str, datetime]:
        """根据刷新令牌生成新的访问令牌。

        当前仓库没有暴露调用此方法的接口；它用于理解“刷新令牌换访问令牌”的
        分层位置，后续新增接口前应先补充校验与测试。
        """
        user_id = await jwt_decode(refresh_token)
        access_new_token, access_new_token_expire_time = await create_access_token(
            str(user_id), refresh_token, multi_login=False
        )
        return access_new_token, access_new_token_expire_time
