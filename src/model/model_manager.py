import numpy as np
from surprise import Dataset, Reader
from surprise import SVD
import logging



class DatasetFactory:
    @classmethod
    def create(clz, df):
        rating_scale  = clz.__rating_scale(df)
        reader        = Reader(rating_scale=rating_scale)
        return Dataset.load_from_df(df, reader)

    @staticmethod
    def __rating_scale(df):
        ratings = np.unique(df['rating'])
        scale = (int(ratings.min()), int(ratings.max()))
        logging.info(f'Rating Scale: {scale}')
        return scale



class ModelManager:
    def __init__(self, model = SVD()): self.model = model

    @property
    def model_name(self): return self.model.__class__.__name__

    def train(self, train_dataset):
        logging.info(f'{self.model_name} Training...')
        self.model.fit(train_dataset.build_full_trainset())
        return self


    def predict(self, user_item_df, progress = 20):
        n_examples = user_item_df.shape[0]
        ratings    = []

        for idx, row in user_item_df.iterrows():
            prediction = self.model.predict(str(row['user_id']), str(row['item_id']))
            ratings.append(prediction.est)

            if idx % int(n_examples / progress) == 0:
                percent = (len(ratings)/n_examples)*100
                if percent > 1:
                    logging.info(f'{self.model_name} Ratings Prediction... {percent:.0f}%')

        return ratings


    def predict_inplase(self, user_item_df, progress = 10):
        user_item_df['rating'] = self.predict(user_item_df)
        return user_item_df