import sys
from loguru import logger
from core.config import get_settings

settings = get_settings()


def setup_logger() -> None:
    logger.remove()

    if settings.app_env =="production":
        logger.add(
            sys.stdout,
            level = settings.log_level,
            serialize = True,
        )
    else:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        logger.add(
            sys.stdout,
            format = log_format,
            level= settings.log_level,
            colorize= True,
        )
    
    logger.add(
        "logs/app.log",
        level = "WARNING",
        rotation = "10 MB",
        retention = "7 days",
        serialize = True
    )

setup_logger()

__all__ = ["logger"]

