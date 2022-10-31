class Repository:
    def __init__(self, database):
        self.database = database

    def save(self, row):
        pass

    def save_all(self, df):
        for _, row in df.iterrows():
            self.save(row)