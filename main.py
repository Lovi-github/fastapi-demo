from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.loggerMiddleware import LoggerMiddleware
from core.SingletonMeta import SingletonMeta


from routes.api import router

from settings import settings



class Database(metaclass=SingletonMeta):
    """
    کلاس Database که به عنوان Singleton پیاده‌سازی شده است.
    """

    def __init__(self):
        self.connection_string = "Database Connection Established"

    def connect(self):
        return self.connection_string


class UserService:
    """
    کلاس UserService که وابستگی Database را از طریق Dependency Injection دریافت می‌کند.
    """

    def __init__(self, database: Database):
        self.database = database

    def get_user(self, user_id):
        # فرض کنید که اینجا کارهایی برای دریافت کاربر انجام می‌شود
        return f"User {user_id} fetched using {self.database.connect()}"


def initApplication() -> FastAPI:

    # Create FastApi App
    fastApiApp = FastAPI()

    fullApiPrefix = str("/%s/%s" % (settings.apiPrefix, settings.apiVersion))
    # Mapping api routes
    fastApiApp.include_router(router, prefix=fullApiPrefix)

    # Custom Middlewares
    fastApiApp.add_middleware(LoggerMiddleware)

    # Allow cors
    fastApiApp.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    db_instance = Database()

    user_service = UserService(database=db_instance)

    # دریافت کاربر
    print(user_service.get_user(1))

    return fastApiApp


app = initApplication()
