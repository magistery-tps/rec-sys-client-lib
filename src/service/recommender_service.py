import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging
from enum import Enum
import api
import mapper


class RecommenderService:
    def __init__(self, repository):
        self.__repository = repository


    def upsert(
        self,
        name                   : str,
        user_similarity_matrix : mapper.Model,
        item_similarity_matrix : mapper.Model
    ):
        models = self.__repository.find(query={'name': name})

        if len(models) > 0 and models[0].name == name:
            logging.info(f'Already exists {name} recommender.')
            model = models[0]
            model.user_similarity_matrix = user_similarity_matrix.id
            model.item_similarity_matrix = item_similarity_matrix.id
            return self.__repository.update(model)
        else:
            logging.info(f'Insert {name} recommender.')
            model = mapper.Model({
                'name': name,
                'user_similarity_matrix': user_similarity_matrix.id,
                'item_similarity_matrix': item_similarity_matrix.id
            })
            return self.__repository.add(model)


    def update(self, model): return self.__repository.update(model)
