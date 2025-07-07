import sys
import os

from loguru import logger as loguru_logger


def get_log_path():
    # 兼容 PyInstaller 打包和开发环境
    if hasattr(sys, '_MEIPASS'):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(".")
    log_dir = os.path.join(base_dir, "data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "system.log")

class Loggin:
    def __init__(self) -> None:
            self.level = "DEBUG"
       

    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=sys.stdout, level=self.level)

        # 将日志同时输出到 data/logs 目录
        loguru_logger.add(
            get_log_path(),
            level=self.level,
            rotation="100 MB",
            retention="7 days",
            enqueue=True,
            encoding="utf-8",
        )
        return loguru_logger


loggin = Loggin()
logger = loggin.setup_logger()
