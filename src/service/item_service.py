import numpy as np
import api
from repository import ItemRepository
import util as ut
import seaborn as sns
import multiprocessing as mp
import pandas as pd
from logger import get_logger


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self._logger    = get_logger(self)

    def find_all(self, page_size = 500):
        return pd.DataFrame.from_records(self.repository.find(page_size=page_size))
