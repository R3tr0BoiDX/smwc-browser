import logging

from source.gui.elements import ScreenLogHandler


class LoggerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance.init_singleton()
        return cls._instance

    def init_singleton(self):
        """Initialize singleton."""
        # pylint: disable=attribute-defined-outside-init
        self.logger = logging.getLogger(__name__)

        # Add handler to log to display log on screen
        self.handler = ScreenLogHandler()
        self.logger.addHandler(self.handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
