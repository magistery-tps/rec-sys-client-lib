from recsys import util as ut
from recsys.logger import get_logger
from abc import ABCMeta, abstractmethod


class Job(metaclass=ABCMeta):
    """Used to execute actions into an airflow server as a DAG or directly from bash. 
    Subclasses implement perform method to define your own actions."
    """
    def __init__(self, ctx):
        self.ctx = ctx
        self._logger = get_logger(self)

    @abstractmethod
    def _perform(self):
        """Code to execute."""
        pass

    def execute(self):
        stopwach = ut.Stopwatch()
        self._logger.info(f'Start')
        self._perform()
        self._logger.info(f'Finish. Elapsed time: {stopwach}')
