"""
Logging configuration for Congress API Explorer.
"""

import logging
import logging.config
from typing import Optional

from .config import settings


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Log level override (defaults to settings.log_level)
        
    Returns:
        Configured logger instance
    """
    log_level = level or settings.log_level
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": settings.log_format
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": "congress_api_explorer.log",
                "mode": "a"
            }
        },
        "loggers": {
            "congress_mcp": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "httpx": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console"]
        }
    }
    
    logging.config.dictConfig(logging_config)
    return logging.getLogger("congress_mcp")


# Global logger instance
logger = setup_logging()