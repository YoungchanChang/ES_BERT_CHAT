config_basic = {
    "version": 1,
    'disable_existing_loggers': True,
    "formatters": {
        "simple": {"format": "[%(name)s] %(message)s"},
        "complex": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(pathname)s:%(funcName)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
            'stream': 'ext://sys.stdout',
        },
        "access": {
            "class": "logging.FileHandler",
            "filename": "access.log",
            "formatter": "complex",
            "level": "INFO",
        },
        "error": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "formatter": "complex",
            "level": "ERROR",
        },
    },
    "loggers": {
        "basic_logger": {"handlers": ["console", "access", "error"], "level": "DEBUG"},
        "parent": {"level": "DEBUG"}, "parent.child": {"level": "DEBUG"},},
}
