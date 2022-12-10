import pandas as pd
import logging
import math


class DataFramPaginationIterator:
    def __init__(self, df: pd.DataFrame, page_size: int=10):
        self.df        = df
        self.page_size = page_size
        self.page_num    = 0
        self.total_pages = math.ceil(self.df.shape[0] / self.page_size)


    def __iter__(self):
        self.page_num    = 0
        self.total_pages = math.ceil(self.df.shape[0] / self.page_size)
        return self


    def __next__(self):
        if self.page_num >= self.total_pages:
            logging.info(f'Totals - Pages {self.total_pages} - Items {self.df.shape[0]}')
            raise StopIteration


        offset = self.page_num * self.page_size


        if (offset + self.page_size) > self.df.shape[0]:
            n_items = self.df.shape[0] - offset
            page    = self.df[offset:offset + n_items]

            logging.info(f'Page {self.page_num+1}/{self.total_pages} - Items {n_items}/{ self.df.shape[0]}')
        else:
            n_items = offset + self.page_size
            page    = self.df[offset:n_items]

            logging.info(f'Page {self.page_num+1}/{self.total_pages} - Items {n_items}/{ self.df.shape[0]}')

        self.page_num += 1

        return page
