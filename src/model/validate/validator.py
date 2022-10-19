import data as dt
import data.dataset as ds
from .validator_summary import ValidatorSummary
import torch
import torch.multiprocessing as mp
import os


class Validator:
    def __init__(self, n_samples, batch_size, metrics, predictors, n_processes=5, target_transform_fn = lambda it: it.squeeze(1)):
        self.n_samples   = n_samples
        self.batch_size  = batch_size
        self.metrics     = metrics
        self.predictors  = predictors
        self.n_processes = n_processes
        self.target_transform_fn = target_transform_fn

    def __evaluate(self, y_true, X, sample, kwargs):
        summary = []
        for p in self.predictors:
            y_pred = p.predict_batch(X, **kwargs)
            result = { 'predictor': p.name, 'sample': sample}
            for m in self.metrics:
                result.update(m.perform(y_pred, y_true, X))
                summary.append(result)
        return summary


    def validate(self, ds, **kwargs):
        summary = []
        with dt.progress_bar(self.n_samples) as bar:
            for sample in range(self.n_samples):
                X, y_true = ds.sample(self.batch_size)
                y_true    = self.target_transform_fn(y_true)

                for p in self.predictors:
                    summary.extend(self.__evaluate(y_true, X, sample, kwargs))
                bar.update()

        return ValidatorSummary.from_list(summary)