import util as ut
import logging
from abc import ABCMeta, abstractmethod


class Job(metaclass=ABCMeta):
    def __init__(self, ctx): self.ctx = ctx

    @abstractmethod
    def _perform(self):
        pass

    def execute(self):
        stopwach = ut.Stopwatch()
        logging.info(f'Start {self.__class__.__name__}')
        self._perform()
        logging.info(f'Finish {self.__class__.__name__}. Elapsec time: {stopwach}')
