from ..mean_user_at_k_metric import MeanUserAtkMetric
from metric.discretizer import identity
import torch


def APK(y_true, k):
    tp_total = torch.sum(y_true)
    if tp_total == 0: return torch.tensor(0.0)
    return sum([v / (i+1) for i, v in enumerate(y_true)]) / min(k, tp_total)


class MeanAveragePrecisionAtk(MeanUserAtkMetric):
    def __init__(self, user_index, k=10, decimals=4, discretizer=identity(), rating_decimals=0):
        super().__init__('mAP@' , user_index, k, decimals, discretizer, rating_decimals)

    def _score(self, y_pred, y_true):
        return APK(y_true, self._k)
