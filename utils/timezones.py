"""项目统一使用的时区时间工具。"""

import datetime

import pytz

from settings import settings


class TimeZoneUtils:
    """将 settings.DATETIME_TIMEZONE 封装为可复用的时间与转换方法。"""

    def __init__(self, timezone_str=settings.DATETIME_TIMEZONE):
        self.timezone = pytz.timezone(timezone_str)

    def get_timezone_datetime(self) -> datetime.datetime:
        """返回当前配置时区的带时区时间。"""
        return datetime.datetime.now(self.timezone)

    def get_timezone_timestamp(self) -> int:
        """返回当前配置时区对应的秒级时间戳。"""
        return int(self.get_timezone_datetime().timestamp())

    def get_timezone_milliseconds(self) -> int:
        """返回当前配置时区对应的毫秒级时间戳。"""
        return int(self.get_timezone_datetime().timestamp() * 1000)

    def datetime_to_timezone_str(
        self,
        dt: datetime.datetime,
        format_str: str = settings.DATETIME_FORMAT,
    ) -> str:
        """将时间对象转换为当前时区的格式化字符串。"""
        return dt.astimezone(self.timezone).strftime(format_str)

    def datetime_to_timezone_datetime(self, dt: datetime.datetime) -> datetime.datetime:
        """将给定时间转换为当前配置时区的时间对象。"""
        return dt.astimezone(self.timezone)

    @staticmethod
    def datetime_to_timezone_utc(dt: datetime.datetime) -> datetime.datetime:
        """将带时区时间转换为 UTC 时间对象。"""
        return dt.astimezone(pytz.utc)

    def datetime_to_timezone_timestamp(self, dt: datetime.datetime) -> int:
        """将时间转换为当前配置时区的秒级时间戳。"""
        return int(dt.astimezone(self.timezone).timestamp())

    def datetime_to_timezone_milliseconds(self, dt: datetime.datetime) -> int:
        """将时间转换为当前配置时区的毫秒级时间戳。"""
        return int(dt.astimezone(self.timezone).timestamp() * 1000)

    def str_to_timezone_utc(
        self,
        time_str: str,
        format_str: str = settings.DATETIME_FORMAT,
    ) -> datetime.datetime:
        """按指定格式解析字符串，并转换成 UTC 时间。"""
        dt = datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)
        return self.datetime_to_timezone_utc(dt)

    def str_to_timezone_datetime(
        self,
        time_str: str,
        format_str: str = settings.DATETIME_FORMAT,
    ) -> datetime.datetime:
        """按指定格式解析字符串，并附加当前配置时区。"""
        return datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)

    def utc_datetime_to_timezone_datetime(self, utc_time: datetime.datetime) -> datetime.datetime:
        """将 UTC 时间对象转换为当前配置时区。"""
        return utc_time.replace(tzinfo=pytz.utc).astimezone(self.timezone)

    def utc_timestamp_to_timezone_datetime(self, timestamp: int) -> datetime.datetime:
        """将 UTC 秒级时间戳转换为当前配置时区的时间对象。"""
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        return self.datetime_to_timezone_datetime(utc_datetime)

    def get_timezone_expire_time(self, expires_delta: datetime.timedelta) -> datetime.datetime:
        """根据时间间隔计算配置时区中的到期时间。"""
        return self.get_timezone_datetime() + expires_delta

    def get_timezone_expire_seconds(self, expire_datetime: datetime.datetime) -> int:
        """计算到期时间距离当前配置时区时间的剩余秒数。

        已过期时返回 0，便于调用方直接判断剩余有效期。
        """
        timezone_datetime = self.get_timezone_datetime()
        expire_datetime = self.datetime_to_timezone_datetime(expire_datetime)
        if expire_datetime < timezone_datetime:
            return 0
        return int((expire_datetime - timezone_datetime).total_seconds())


# JWT 和日志中间件共享同一个时区工具实例。
timezone_utils = TimeZoneUtils()
