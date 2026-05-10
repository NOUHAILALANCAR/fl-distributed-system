from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
           colorize=True, level="INFO")
logger.add("fl_system.log", rotation="10 MB", level="DEBUG")
