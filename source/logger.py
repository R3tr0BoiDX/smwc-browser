import logging

from source.gui.elements import ScreenLogHandler

DEFAULT_LOG_LEVEL = logging.INFO


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
        self.logger.setLevel(DEFAULT_LOG_LEVEL)

        # Add handler to log to display log on screen
        self.handler = ScreenLogHandler()
        self.logger.addHandler(self.handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the logger.
        In theory this is not needed, as the logger attribute is publicly accessible.
        Reconsider if this is the preferred way to do it.

        Returns:
            logging.Logger: The logger.
        """
        return self.logger
