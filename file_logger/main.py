

from destinations import FileDestination
from logger import CustomLogger, LogLevel
from test import log_somefn


logger = CustomLogger.get_logger(__name__)

logger.add_destination(FileDestination("./logs.txt"), levels=[LogLevel.ERROR])
logger.add_destination(FileDestination("./info_log.txt"), levels=[LogLevel.INFO])



logger.error("This is an error text")
logger.info("This is a info text")
logger.error("Hi this is an error text")

log_somefn()