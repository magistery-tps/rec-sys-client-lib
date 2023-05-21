import logging


class LoggerBuilder:
    """Builder object use to config main logger.
    """
    @staticmethod
    def build(
        path           = './logger.log',
        message_format = '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s',
        level          = logging.INFO
    ):
        """Config main logger.

        Args:
            path (str, optional): Output logging file path. Defaults to './logger.log'.
            message_format (str, optional): Log message format. Defaults to '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'.
            level (logging.LEVEL, optional): Login level. Defaults to logging.INFO.
        """
        logging.basicConfig(
            level    = level,
            format   = message_format,
            handlers = [
                logging.FileHandler(path),
                logging.StreamHandler()
            ]
        )

def get_logger(object):
    """Get a logger instance for a specific object class. It's allows log messages with the current class name as prefix.

    Args:
        object (object): Any object instance.

    Returns:
        Logger: a logger instance using arg object class name as log message prefix.
    """
    return logging.getLogger(object.__class__.__name__)