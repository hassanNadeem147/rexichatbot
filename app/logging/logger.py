from pathlib import Path
import sys

from loguru import logger


# Project root / logs folder
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# Remove default Loguru console handler
logger.remove()


# Configure log level colors
logger.level("INFO", color="<white>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<fg #8B0000>")


# Console Output
logger.add(
    sys.stdout,
    format=(
        "<fg #808080>{time:YYYY-MM-DD HH:mm:ss}</fg #808080> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<blue>{function}</blue>:"
        "<fg #808080>{line}</fg #808080> - "
        "<level>{message}</level>"
    ),
    level="INFO",
)


# Info and Warning file
logger.add(
    LOG_DIR / "app_info.log",
    level="INFO",
    filter=lambda record: record["level"].name in ["INFO", "WARNING"],
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} - {message}"
    ),
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)


# Error file
logger.add(
    LOG_DIR / "app_error.log",
    level="ERROR",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} - {message}"
    ),
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)