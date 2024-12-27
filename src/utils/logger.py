import sys

from loguru import logger as _logger

# sys.stdout.reconfigure(encoding='utf-8')

_logger.add(
    sys.stdout,
    # enqueue=True,
    colorize=True,
    # diagnose=True,
    # backtrace=True,
)

logger = _logger
