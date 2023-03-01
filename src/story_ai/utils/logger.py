import os
import sys
from datetime import datetime, timedelta, time, timezone
from typing import Set

from loguru import logger

LOGGER_LVL_SET: Set[str] = {"debug", "info", "warning", "error", "critical"}

logger.remove()  # Default "sys.stderr" sink is not picklable


def create_log_file(log_root, log_type):
    folder = os.path.dirname(os.path.abspath(log_root))
    os.makedirs(folder, exist_ok=True)
    return os.path.join(log_root, f"{log_type}.log")


class Rotator:
    def __init__(self, *, size, at):
        now = datetime.now()
        self._size_limit = size
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)

        if now >= self._time_limit:
            self._time_limit += timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        if message.record["time"].timestamp() > self._time_limit.timestamp():
            self._time_limit += timedelta(days=1)
            return True
        return False


def create_logger(log_root, enable_file_log=True, enable_console_log=False):
    logger.remove()
    if enable_console_log:
        logger.add(sys.stderr, level="DEBUG", enqueue=True)
    if enable_file_log:
        rotator = Rotator(size=5e8, at=time(0, 0, 0, tzinfo=timezone.utc))
        for lvl in LOGGER_LVL_SET:
            logger.add(
                create_log_file(log_root, lvl),
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                rotation=rotator.should_rotate,
                level=lvl.upper(),
                enqueue=True,
                encoding="utf8",
                # serialize=True,
            )

        return logger
