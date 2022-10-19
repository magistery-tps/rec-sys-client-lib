from ..clasification_metric import ClasificationMetric
from metric.discretizer import identity
import torchmetrics


class FBetaScore(ClasificationMetric):
    def __init__(self, num_classes=None, average='macro', beta=1, decimals=4, discretizer=identity()):
        super().__init__(
            f'F{beta}Score({average})', 
            torchmetrics.FBetaScore(num_classes=num_classes, average=average, beta=beta),
            decimals, 
            discretizer
        )
