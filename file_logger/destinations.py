from abc import ABC, abstractmethod
import json


class LogDestination(ABC):

    @abstractmethod
    def log_message(self, name: str, message="", data=None):
        pass

    def _format_log(self, name: str, message="", data=None):
        log_msg = f"{name}: {message}"

        if data:
            log_msg += json.dumps(data, indent=4)
            
        return log_msg


class DefaultDestination(LogDestination):

    def log_message(self, name: str, message="", data=None):
        log_msg = self._format_log(name, message, data)
        print(log_msg)


class FileDestination(LogDestination):
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        super().__init__()

    def log_message(self, name, message="", data=None):
        log_msg = self._format_log(name, message, data)

        with open(self.log_file_path, "a") as f:
            # f.seek(0, 2)

            f.writelines(log_msg + "\n")
