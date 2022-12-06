import numpy as np
from surprise import Dataset, Reader
from surprise import SVD
from IPython.display import clear_output
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

    
    def train(self, train_dataset):
        self.model.fit(train_dataset.build_full_trainset())
        return self


    def predict(self, user_item_df, progress_each = 100000):
        ratings = []
        for idx, row in user_item_df.iterrows():
            ratings.append(self.model.predict(str(row['user_id']), str(row['item_id'])).est)
            if idx % progress_each == 0:
                clear_output(wait=True)
                percent = (len(ratings)/user_item_df.shape[0])*100
                logging.info(f'Prediction: {percent:.0f}%')
        return ratings


    def predict_inplase(self, user_item_df, progress_each = 100000):
        user_item_df['rating'] = self.predict(user_item_df)
        return user_item_df