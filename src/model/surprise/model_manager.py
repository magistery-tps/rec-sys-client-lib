import numpy as np
import tqdm
from logger import get_logger
from surprise import Dataset, Reader
from surprise import SVD


class DatasetFactory:
    def __init__(self):
        self._logger = get_logger(self)

    def create(
            self,
            df,
            columns=('user_seq', 'item_seq', 'rating')
    ):
        rating_scale = self.__rating_scale(df, columns)
        reader = Reader(rating_scale=rating_scale)
        return Dataset.load_from_df(df[list(columns)], reader)

    def __rating_scale(self, df, columns):
        ratings = np.unique(df[columns[2]])
        scale = (int(ratings.min()), int(ratings.max()))
        self._logger.info(f'{columns[2].capitalize()} Scale: {scale}')
        return scale


class ModelManager:
    def __init__(self, model=SVD()):
        self.model = model
        self._logger = get_logger(self)

    @property
    def model_name(self): return self.model.__class__.__name__

    def train(self, train_dataset):
        self._logger.info(f'{self.model_name} Training...')
        self.model.fit(train_dataset.build_full_trainset())
        return self

    def predict(
            self,
            user_item_df,
            columns=('user_seq', 'item_seq', 'value')
    ):
        self._logger.info(f'{self.model_name} Predictions...')

        ratings = []
        for idx, row in tqdm.tqdm(user_item_df.iterrows(), total=user_item_df.shape[0]):
            user_seq = str(row[columns[0]])
            item_seq = str(columns[1])

            prediction = self.model.predict(user_seq, item_seq).est

            ratings.append(prediction)

        return ratings

    def predict_inplase(
            self,
            user_item_df,
            columns=('user_seq', 'item_seq', 'value')
    ):
        user_item_df['rating'] = self.predict(user_item_df, columns)
        return user_item_df
