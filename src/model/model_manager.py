from surprise import Dataset, Reader
from surprise import SVD
from IPython.display import clear_output
import logging


class ModelManager:
    def __init__(
        self, 
        file_path,
        file_line_format = "user item rating",
        file_sep         = ",",
        model            = SVD()
    ):
        reader     = Reader(
            line_format = file_line_format, 
            sep         = file_sep
        )
        self.data  = Dataset.load_from_file(file_path, reader=reader)
        self.model = model


    def train(self):
        self.model.fit(self.data.build_full_trainset())


    def predict(self, user_item_df, progress_each = 100000):
        ratings = []
        for idx, row in user_item_df.iterrows():
            ratings.append(self.model.predict(str(row['user_id']), str(row['item_id'])).est)
            if idx % progress_each == 0:
                clear_output(wait=True)
                percent = (len(ratings)/user_item_df.shape[0])*100
                logging.info(f'Prediction progress: {percent:.0f}%')
        return ratings