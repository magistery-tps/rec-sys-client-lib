from ..abstract_metric import AbstractMetric
from metric.discretizer import identity
import torch
import util as ut


class ClasificationMetric(AbstractMetric):
    def __init__(self, name, metric, decimals=4, discretizer=identity()):
        super().__init__(name, decimals)
        self.__metric = metric
        self.__discretizer_fn = discretizer.closure()

    def _calculate(self, y_pred, y_true, X):
        y_pred_ = ut.apply(y_pred, self.__discretizer_fn).int()
        y_true_ = ut.apply(y_true, self.__discretizer_fn).int()

        return (self.__metric(y_pred_, y_true_),)
