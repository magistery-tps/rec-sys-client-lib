import logging


class LoggerBuilder:
    @staticmethod
    def build(
        path           = '../../logger.log', 
        message_format = '%(asctime)s [%(levelname)s] %(message)s', 
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