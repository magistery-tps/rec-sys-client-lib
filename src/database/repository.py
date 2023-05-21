class Repository:
    def __init__(self, database):
        self.database = database

    def save(self, row):
        """ Insert rows into rec-sys database."""
        pass

    def save_all(self, df):
        """ Insert all pd.DataFrame rows into rec-sys database."""
        for _, row in df.iterrows():
            self.save(row)