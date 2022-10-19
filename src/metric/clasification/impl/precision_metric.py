from ..clasification_metric import ClasificationMetric
from metric.discretizer import identity
import torchmetrics


class Precision(ClasificationMetric):
    def __init__(self, num_classes=None, average='macro', decimals=4, discretizer=identity()):
        super().__init__(
            f'Precision({average})', 
            torchmetrics.Precision(num_classes=num_classes, average=average),
            decimals, 
            discretizer
        )
