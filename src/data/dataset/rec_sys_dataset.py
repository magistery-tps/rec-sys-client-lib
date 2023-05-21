import torch
from torch.utils.data import Dataset
import pandas as pd
import data as dtypes
import data as dt
import numpy as np
from logger import get_logger


class RecSysDataset(Dataset):
    def __init__(self, dataset, transform , target_transform, device):
        self._dataset          = dataset
        self._transform        = transform,
        self._target_transform = target_transform
        self._device           = device
        self._logger           = get_logger(self)

    def __len__(self): return len(self.data)

    def __getitem__(self, rows_idx):
        try:
            return self._to_feats_target(self.data.iloc[rows_idx, :])
        except Exception as e:
            self._logger.error(f'Error to index dataset with: {rows_idx}. dataset size: {len(self.data)}')
            raise e


    def sample(self, size):
        indexes = torch.randint(0, len(self)-1, (size,))
        df_sample = pd.DataFrame(self.data.iloc[indexes, :])
        features, target = self._to_feats_target(df_sample)
        return features, target

    def subset_by_indexes(self, indexes):
        return RecSysDataset(
            dataset          = self.data.iloc[indexes, :],
            transform        = self._transform[0],
            target_transform = self._target_transform,
            device           = self._device
        )

    @property
    def data(self): return self._dataset


    @property
    def columns(self): return self.data.columns


    @property
    def dtypes(self): return self.data.dtypes


    @property
    def info(self): return self.data.info()


    @property
    def shape(self): return self.data.shape


    @property
    def features(self): return self._to_feats(self.data)


    @property
    def targets(self): return self._to_target(self.data)


    @property
    def features_uniques(self):
        return [c[0] for c in self.features_value_counts]


    @property
    def target_uniques(self): return self.targets_value_counts[0]


    @property
    def features_value_counts(self):
        features = self.features
        return np.array([ np.unique(features[:, col_idx].cpu().numpy(), return_counts=True) for col_idx in range(features.shape[1])], dtype=object)


    @property
    def targets_value_counts(self):
        return np.unique(self.targets.numpy(), return_counts=True)

    def _to_feats_target(self, observations):
        features    = self._to_feats(observations)
        target      = self._to_target(observations)

        return features, target


    def _to_feats(self, observations):
        return self._transform[0](observations, self._device)


    def _to_target(self, observations):
        return self._target_transform(observations, self._device)
