from logger import CustomLogger


logger = CustomLogger.get_logger(__name__)


def log_somefn():
    logger.debug("HELLO FROM TEST")