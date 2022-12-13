import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging
from enum import Enum
import api
import mapper


class SimilarityMatrixService:
    def __init__(self, matrix_repository, cell_repository):
        self.__matrix_repository = matrix_repository
        self.__cell_repository   = cell_repository


    def create_or_get(
        self,
        name : str,
        type : api.SimilarityMatrixType,
        desc : str = None
    ):
        if desc is None:
            desc = name

        models = self.__matrix_repository.find(query={'name': name, 'type': str(type.value)})

        if len(models) > 0 and models[0].name == name:
            logging.info(f'{name} of type {type} already exists!')
            return models[0]
        else:
            logging.info(f'Insert {name} of type {type}.')
            return self.__matrix_repository.add(name, type, desc)

    def update(self, model):
        return self.__matrix_repository.update(model.id, model.name, model.type, model.description, model.version)


    def add_cells(self, matrix: mapper.Model, cells: pd.DataFrame, page_size=10_000):
        cells['matrix']  = matrix.id
        cells['version'] = matrix.version

        iterator = ut.DataFramPaginationIterator(cells, page_size=page_size)
        [self.__cell_repository.bulk_add(page) for page in iterator]

