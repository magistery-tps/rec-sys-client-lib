from model.predictor.predictor import AbstractPredictor
import torch


class CachedPredictor(AbstractPredictor):
    def __init__(self, predictor):
        self._predictor = predictor
        self._cache = {}

    @property
    def name(self): return self._predictor.name

    def predict(self, user_idx, item_idx, n_neighbors=10, debug=False):        
        key = f'{user_idx}-{item_idx}'
        if key in self._cache:
            return self._cache[key]
        else:
            y_pred = self._predictor.predict(user_idx, item_idx, n_neighbors=10, debug=debug)
            self._cache[key] = y_pred
            return y_pred