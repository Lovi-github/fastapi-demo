"""运行配置。

Settings 会读取项目根目录的 .env；环境变量不存在时使用本文件默认值。
默认密钥仅适合演示，真实项目必须由本机 .env 或部署平台的密钥管理覆盖。
"""

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """集中定义 FastAPI、日志和 JWT 的可配置项。"""
    app_name: str = "Fast Api Project Name"
    debug: bool = True
    secret_key: str = ''
    apiPrefix  : str = "api"
    apiVersion : str = "v1"
    ALLOWED_HOSTS : list = []

    DATETIME_TIMEZONE: str = 'Asia/Tehran'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    LOG_STDOUT_FILENAME: str = 'fapi_log_access.log'
    LOG_STDERR_FILENAME: str = 'fapi_log_error.log'

    # 访问令牌默认有效期：86400 秒，即 24 小时。
    TOKEN_EXPIRE_SECONDS : int = 86400
    TOKEN_SECRET_KEY : str = 'jwt_secret_key'
    TOKEN_ALGORITHM : str = 'HS256'

    class Config:
        # 不提交 .env；它只用于覆盖本机或部署环境中的默认配置。
        env_file = ".env"

settings = Settings()
