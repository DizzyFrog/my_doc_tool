import sys

from loguru import logger as loguru_logger




class Loggin:
    def __init__(self) -> None:
            self.level = "DEBUG"
       

    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=sys.stdout, level=self.level)

        # 将日志同时输出到文件
        loguru_logger.add(
            "logs/system.log",
            level=self.level,
            rotation="100 MB",
            retention="7 days",
            enqueue=True,
            encoding="utf-8",
        )
        return loguru_logger


loggin = Loggin()
logger = loggin.setup_logger()
