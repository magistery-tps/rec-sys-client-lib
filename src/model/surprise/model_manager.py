import numpy as np
from surprise import Dataset, Reader
from surprise import SVD
from logger import get_logger



class DatasetFactory:
    def __init__(self):
        self._logger = get_logger(self)

    def create(
        self,
        df,
        columns = ('user_seq', 'item_seq', 'rating')
    ):
        rating_scale  = self.__rating_scale(df, columns)
        reader        = Reader(rating_scale=rating_scale)
        return Dataset.load_from_df(df[list(columns)], reader)

    def __rating_scale(self, df, columns):
        ratings = np.unique(df[columns[2]])
        scale = (int(ratings.min()), int(ratings.max()))
        self._logger.info(f'{columns[2].capitalize()} Scale: {scale}')
        return scale



class ModelManager:
    def __init__(self, model = SVD()):
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
        columns  = ('user_seq', 'item_seq', 'value'),
        progress = 10
    ):
        n_examples = user_item_df.shape[0]
        ratings    = []

        for idx, row in user_item_df.iterrows():
            prediction = self.model.predict(str(row[columns[0]]), str(columns[1]))
            ratings.append(prediction.est)

            if idx % int(n_examples / progress) == 0:
                percent = (len(ratings)/n_examples)*100
                if percent > 1:
                    self._logger.info(f'{self.model_name} {columns[2].capitalize()} Prediction... {percent:.0f}%')

        return ratings


    def predict_inplase(
        self,
        user_item_df,
        columns  = ('user_seq', 'item_seq', 'value'),
        progress = 10
    ):
        user_item_df['rating'] = self.predict(user_item_df, columns, progress)
        return user_item_df