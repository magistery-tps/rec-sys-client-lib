from random import sample
import logging
import torch
import numpy as np
import util as ut


class UserYPredYTrueSampler:
    def __init__(self, user_index, sample_size, decimals=0):
        self.__user_index = user_index
        self.__sample_size = sample_size
        self.__decimals = decimals

    def sample(self, y_true, y_pred, X):
        user_seq = X[:, self.__user_index]

        for user_idx in torch.unique(user_seq):
            y_true_sample, y_pred_sample = \
                self.__y_true_y_pred_sample_by_user_idx(y_true, y_pred, user_seq, user_idx)

            if y_true_sample == None:
                continue

            indexes_desc_by_val = torch.argsort(y_true_sample, dim=0, descending=True) 

            yield y_true_sample[indexes_desc_by_val], y_pred_sample[indexes_desc_by_val]

    def __y_true_y_pred_sample_by_user_idx(self, y_true, y_pred, user_seq, user_idx):
        indexes = ut.indexes_of(user_seq, user_idx)

        if indexes.size()[0] < self.__sample_size:
            return None, None

        indexes_sample = ut.random_choice(indexes, self.__sample_size)

        y_true_sample = torch.index_select(y_true, dim=0, index=indexes_sample)
        if not ut.is_int(y_true_sample):
            y_true_sample = torch.round(y_true_sample, decimals=self.__decimals)

        y_pred_sample = torch.index_select(y_pred, dim=0, index=indexes_sample)
        if not ut.is_int(y_pred_sample):
            y_pred_sample = torch.round(y_pred_sample, decimals=self.__decimals)

        return y_true_sample, y_pred_sample
