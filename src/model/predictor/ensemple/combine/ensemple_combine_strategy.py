from abc import ABC
import torch


class EnsempleCombineStrategy(ABC):
    def combine(self, y_preds: list[torch.Tensor]):
        pass