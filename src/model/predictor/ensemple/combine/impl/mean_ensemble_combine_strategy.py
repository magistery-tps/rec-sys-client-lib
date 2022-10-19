from ..ensemple_combine_strategy import EnsempleCombineStrategy
from abc import ABC
import torch


class MeanEnsempleCombineStrategy(EnsempleCombineStrategy):
     def combine(self, y_preds: list[torch.Tensor]):
        stacked_y_preds = torch.stack(y_preds)
        return torch.mean(stacked_y_preds.float(), dim=0)
