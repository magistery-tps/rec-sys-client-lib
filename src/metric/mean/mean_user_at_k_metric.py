from ..abstract_metric import AbstractMetric
from metric.discretizer import identity
from .user_pred_true_sampler import UserYPredYTrueSampler
import logging
import torch


class MeanUserAtkMetric(AbstractMetric):
    def __init__(self, name, user_index, k=10, decimals=4, discretizer=identity(), rating_decimals=0):
        super().__init__(f'{name}{k}{discretizer.desc}', decimals)
        self.__sampler     = UserYPredYTrueSampler(user_index, k, rating_decimals)
        self.__discretizer_fn = discretizer.closure()
        self._k           = k

    def _calculate(self, y_pred, y_true, X):
        scores = []
        for y_pred_sample, y_true_sample in self.__sampler.sample(y_pred, y_true, X):
            y_pred_sample = y_pred_sample.apply_(self.__discretizer_fn).int()
            y_true_sample = y_true_sample.apply_(self.__discretizer_fn).int()

            scores.append(self._score(y_pred_sample, y_true_sample).item())

        n_users_found = len(scores)
        logging.debug(f'n_users_found: {len(scores)}')
        return torch.mean(torch.tensor(scores)), n_users_found

    def _score(self, y_pred, y_true):
        pass

    def _build_result(self, metrics):
        return {
            self.name: metrics[0],
            f'{self.name} users found': metrics[1]
        }
