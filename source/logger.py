import logging

# from source.gui.elements import ScreenLogger


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
        self.shared_logger = logging.getLogger(__name__)

        # todo: Add handler to log to display log on screen
        # handler = ScreenLogHandler()
        # LoggerManager().logger().addHandler(handler)

    def logger(self) -> logging.Logger:
        return self.shared_logger
