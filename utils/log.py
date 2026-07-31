"""基于 Loguru 的文件日志初始化。"""

from __future__ import annotations
import os
from typing import TYPE_CHECKING
from pathlib import Path
from loguru import logger
from settings import settings

if TYPE_CHECKING:
    import loguru

BasePath = Path(__file__).resolve().parent.parent


class Logger:
    """创建日志目录，并配置 INFO 与 ERROR 两个日志输出。"""
    def __init__(self):
        self.log_path =os.path.join(BasePath,'logs')

    def log(self) -> loguru.Logger:
        """返回已配置的 Loguru logger。

        模块导入时会执行本方法，因此 logs/ 目录和日志 sink 会在应用启动前准备好。
        """
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        log_stdout_file = os.path.join(self.log_path, settings.LOG_STDOUT_FILENAME)
        log_stderr_file = os.path.join(self.log_path, settings.LOG_STDERR_FILENAME)

        log_config = dict(rotation='10 MB', retention='15 days', compression='tar.gz', enqueue=True)

        logger.add(
            log_stdout_file,
            level='INFO',
            filter=lambda record: record['level'].name == 'INFO' or record['level'].no <= 25,
            **log_config,
            backtrace=False,
            diagnose=False,
        )

        logger.add(
            log_stderr_file,
            level='ERROR',
            filter=lambda record: record['level'].name == 'ERROR' or record['level'].no >= 30,
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        return logger


# LoggerMiddleware 导入此对象后即可记录请求，不需要每次请求重复配置 sink。
log = Logger().log()
