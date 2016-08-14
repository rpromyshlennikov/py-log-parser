import logging
from logging.config import dictConfig

from py_log_parser import settings


logging.getLogger("paramiko.transport").setLevel(logging.WARNING)

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "base_handler": {"class": "logging.StreamHandler",
                         "formatter": "standard"}
    },
    "loggers": {
        "": {
            "handlers": ["base_handler"],
            "level": settings.console_log_level,
        },
    },
}

dictConfig(logging_config)
