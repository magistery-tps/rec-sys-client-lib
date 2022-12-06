import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging


class RatingMatrixService:
    def __init__(self, interaction_service):
        self.__interaction_service = interaction_service


    def compute(self, train_interactions, model):
        future_interactions = self.__interaction_service.unrated_distinct_user_item(train_interactions)

        logging.info(f'Train model and predict future interactions({future_interactions.shape[0]})...')

        train_dataset = ml.DatasetFactory.create(train_interactions)

        ml.ModelManager(model).train(train_dataset).predict_inplase(future_interactions)

        all_interactions = ut.concat(train_interactions, future_interactions)

        logging.info('Compute interactions sparse matrix...')
        return self.__interaction_service.to_matrix(all_interactions)