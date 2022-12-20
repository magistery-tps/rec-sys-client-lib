import logging


class LoggerBuilder:
    @staticmethod
    def build(
        path           = './logger.log',
        message_format = '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s',
        level          = logging.INFO
    ):
        logging.basicConfig(
            level    = level,
            format   = message_format,
            handlers = [
                logging.FileHandler(path),
                logging.StreamHandler()
            ]
        )

def get_logger(object): return logging.getLogger(object.__class__.__name__)