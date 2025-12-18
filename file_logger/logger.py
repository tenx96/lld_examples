from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
from threading import Lock
from destinations import DefaultDestination, LogDestination


class LogLevel(Enum):
    INFO = "info"
    ERROR = "error"
    DEBUG = "debug"
    SUCCESS = "success"


LOG_LEVELS = list(LogLevel)


@dataclass
class LoggerConfig:
    destinations: Dict[LogLevel, List[LogDestination]]


class CustomLogger:
    _config_instance: LoggerConfig = None
    _lock = Lock()
    _logger_store = {}

    def __init__(self, name: str, configuration: LoggerConfig = None):
        self.configuration = configuration
        self.name = name

    @classmethod
    def get_logger(cls, name: str) -> "CustomLogger":
        conf = cls._get_config_instance()
        
        if name not in cls._logger_store:
            with cls._lock:
                if not name in cls._logger_store:
                    cls._logger_store[name] = cls(name, conf)
        
        return cls._logger_store[name]


    @classmethod
    def _get_config_instance(cls):
        if not cls._config_instance:
            with cls._lock:
                if not cls._config_instance:
                    default_destination = DefaultDestination()
                    destinations = defaultdict(list)  # INFO -> [Destinations]
                    for level in LOG_LEVELS:
                        destinations[level].append(default_destination)

                    cls._config_instance = LoggerConfig(destinations=destinations)

        return cls._config_instance

    def add_destination(self, *dest: LogDestination, levels: List[LogLevel] = None ):
        with self._lock:
            for level in levels or LOG_LEVELS:
                for d in dest:
                    self._get_config_instance().destinations[level].append(d)

    def info(self, message="", data=None):
        self.__log_message(LogLevel.INFO, message, data)

    def error(self, message="", data=None):
        self.__log_message(LogLevel.ERROR, message, data)

    def debug(self, message="", data=None):
        self.__log_message(LogLevel.DEBUG, message, data)

    def success(self, message="", data=None):
        self.__log_message(LogLevel.SUCCESS, message, data)

    def _get_destinations_for_log_level(self, level: LogLevel) -> List[LogDestination]:
        return self.configuration.destinations[level]

    def __log_message(self, level=LogLevel.INFO, message="", data=None):
        destinations = self._get_destinations_for_log_level(level)
        for d in destinations:
            d.log_message(self.name, message=message, data=data)
