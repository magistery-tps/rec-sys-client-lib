from abc import ABC
import torch
import util as ut


class AbstractMetric(ABC):
    def __init__(self, name, decimals=4):
        self.name = name
        self._decimals = decimals

    def perform(self, y_pred, y_true, X):
        metrics = self._calculate(y_pred, y_true, X)
        metrics = (self.__round(metrics[0]),) + metrics[1:]
        return self._build_result(metrics)

    def _calculate(self, y_pred, y_true, X):
        pass

    def _build_result(self,  metrics):
        return {self.name: metrics[0]}

    def __round(self, value):
        if ut.is_int(value): 
            return torch.round(value, decimals=self._decimals).item()
        return value.item()