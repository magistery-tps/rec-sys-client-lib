import util as ut
from logger import get_logger
from abc import ABCMeta, abstractmethod


class Job(metaclass=ABCMeta):
    def __init__(self, ctx):
        self.ctx = ctx
        self._logger = get_logger(self)

    @abstractmethod
    def _perform(self):
        pass

    def execute(self):
        stopwach = ut.Stopwatch()
        self._logger.info(f'Start')
        self._perform()
        self._logger.info(f'Finish. Elapsed time: {stopwach}')
