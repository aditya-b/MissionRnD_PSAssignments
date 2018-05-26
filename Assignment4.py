from logging import *
from Package1 import *

logger = getLogger(__name__)
lg=getLogger()
logger.setLevel(DEBUG)
sh = FileHandler("C:/Pre Summer Assignments/Main.log")
sh.setLevel(DEBUG)
fh = Formatter("%(levelname)s: %(message)s %(asctime)s")
sh.setFormatter(fh)
logger.addHandler(sh)
logger.info('Entry log of main function')
try:
    Module1.function1()
    Module1.function2()
    Module2.function3()
    Module2.function4()
    Module3.function5()
    Module4.function6()
except Exception as e:
    logger.error(e)
    lg.error(e)
logger.info('Exit log of main function')
d={
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s %(asctime)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },

    "loggers": {
        "a.b": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}