from model.predictor.predictor import AbstractPredictor
import torch
from .combine.ensemple_combine_strategy import EnsempleCombineStrategy
from .combine.impl.mean_ensemble_combine_strategy import MeanEnsempleCombineStrategy


class EnsemplePredictor(AbstractPredictor):
    def __init__(
        self, 
        predictors: list[AbstractPredictor], 
        combine_strategy: EnsempleCombineStrategy = MeanEnsempleCombineStrategy()
    ):
        self._predictors = predictors
        self._combine_strategy = combine_strategy

    @property
    def name(self):
        return f"Ensemple[{', '.join([p.name for p in self._predictors])}]"

    def predict(self, user_idx, item_idx, n_neighbors=10, debug=False):
        y_preds = [p.predict(user_idx, item_idx, debug=debug) for p in self._predictors]
        return self._combine_strategy.combine(y_preds)

    def predict_batch(self, batch, n_neighbors=10, debug=False):
        y_preds = [p.predict_batch(batch, debug=debug) for p in self._predictors]
        return self._combine_strategy.combine(y_preds)
