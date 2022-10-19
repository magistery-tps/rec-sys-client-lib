import pandas as pd
import data.plot as pl
import data as dt
import numpy as np
import matplotlib.pyplot as plt


class ValidatorSummary:

    @staticmethod
    def load(file_path): return ValidatorSummary(pd.read_json(f'{file_path}.json'))

    @staticmethod
    def from_list(metrics_log): return ValidatorSummary(pd.DataFrame(metrics_log))
    
    def save(self, file_path): self.data.to_json(f'{file_path}.json')

    def __init__(self, data): self.data = data

    def __predictor_names(self):
        return np.unique(self.data['predictor'].values)

    def __metric_names(self):
        return set(self.data.columns) - set(['predictor', 'sample'])

    def plot(self, bins=10, show_table = False, show_range = False):
        metric_names    = self.__metric_names()
        predictor_names = self.__predictor_names()

        pl.xl_flat_size()

        for metric_name in metric_names:
            for pre_name in predictor_names:
                pl.describe_num_var(
                    df         = self.data[self.data.predictor == pre_name],
                    column     = metric_name,
                    bins       = bins, 
                    title      = pre_name, 
                    show_table = show_table,
                    show_range = show_range
                )
