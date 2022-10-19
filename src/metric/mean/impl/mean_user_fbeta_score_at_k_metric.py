from ..mean_user_at_k_metric import MeanUserAtkMetric
from metric.discretizer import identity
import torchmetrics


class MeanUserFBetaScoreAtk(MeanUserAtkMetric):
    def __init__(self, user_index, k=10, decimals=4, discretizer=identity(), rating_decimals=0, num_classes=None, average='micro', beta=1):
        name = f'MeanUserF{beta}Score@{k}'
        if average != 'micro':
            name += f'({average})'

        super().__init__(name, user_index, k, decimals, discretizer, rating_decimals)
        self.__metric = torchmetrics.FBetaScore(num_classes=num_classes, average=average, beta=beta)

    def _score(self, y_pred, y_true):
        return self.__metric(y_pred, y_true)
