from ..abstract_metric import AbstractMetric
from math import sqrt
from torchmetrics import MeanSquaredError
import torch


class RMSE(AbstractMetric):
    def __init__(self, decimals=4):
        super().__init__('RMSE', decimals)
        self.__metric = MeanSquaredError()

    def _calculate(self, y_pred, y_true, X):
        return torch.sqrt(self.__metric(y_true, y_pred)),
