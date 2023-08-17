import numpy as np
from recsys.repository import ItemRepository
from recsys import util as unrated_user_item, api
import multiprocessing as mp
import pandas as pd
from recsys.logger import get_logger
from .entity_service import EntityService



class ItemService(EntityService):
    def __init__(self, repository: ItemRepository):
        self.repository = repository
        self._logger    = get_logger(self)


    def find_all(self, page_size = 500):
        """Query all item. Fetch item using a given page size.

        Args:
            page_size (int, optional): Page size use to fetch item. Defaults to 500.

        Returns:
            od.DataFrame: A table of items.
        """
        return pd.DataFrame.from_records(self.repository.find(page_size=page_size))


    def find_by(self, query={}):
        """Query items filtered by field values.

        Args:
            query (dict, optional): A dict of (field_name,field_value) pairs. Defaults to {}.

        Returns:
            od.DataFrame: A table of items.
        """
        return pd.DataFrame.from_records(self.repository.find(query=query))
