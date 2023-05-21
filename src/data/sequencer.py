import pandas as pd


class Sequencer:
    """Used to genera a sequence column from a pre existent column.
    """
    def __init__(self, column, seq_col_name):
        """Constructor

        Args:
            column (str): pre existent column.
            seq_col_name (str): A new columns where generate a numeric sequence.
        """
        self.column = column
        self.seq_col_name = seq_col_name

    def __crete_seq(self, df):
        values = df[self.column].unique()

        seq = 0
        seq_by_value = {}
        for v in values:
            if v in seq_by_value:
                continue
            seq_by_value[v] = seq
            seq += 1
        return seq_by_value

    def perform(self, df):
        """Generate a new numeric sequence column.

        Args:
            df (pd.DataFrame): table where sequence column will appended.

        Returns:
            pd.DataFrame: arg table with new sequence columns.
        """
        seq_by_value = self.__crete_seq(df)
        df[self.seq_col_name] = df[self.column].apply(lambda x: seq_by_value[x])
        return df