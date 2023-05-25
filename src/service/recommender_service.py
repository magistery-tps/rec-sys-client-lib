import numpy as np
import util as ut
import pandas as pd
import model as ml
from logger  import get_logger
from enum import Enum
import api
import mapper


class RecommenderService:
    def __init__(self, repository):
        self.__repository = repository
        self._logger      = get_logger(self)


    def upsert(
        self,
        name                   : str,
        user_similarity_matrix : mapper.Model,
        item_similarity_matrix : mapper.Model
    ):
        """Add or update a recommender.

        Args:
            name (str): Recommender nama. It's an identifier.
            user_similarity_matrix (mapper.Model): A user similarity Matrix Model.
            item_similarity_matrix (mapper.Model): A item similarity Matrix Model.
        """
        models = self.__repository.find(query={'name': name})

        if len(models) > 0 and models[0].name == name:
            self._logger.info(f'Already exists {name} recommender.')
            model = models[0]
            model.user_similarity_matrix = user_similarity_matrix.id
            model.item_similarity_matrix = item_similarity_matrix.id
            return self.__repository.update(model)
        else:
            self._logger.info(f'Insert {name} recommender.')
            model = mapper.Model({
                'name': name,
                'user_similarity_matrix': user_similarity_matrix.id,
                'item_similarity_matrix': item_similarity_matrix.id
            })
            return self.__repository.add(model)
