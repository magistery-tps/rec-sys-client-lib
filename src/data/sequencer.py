import pandas as pd


class Sequencer:
    def __init__(self, column, seq_col_name):
        self.column = column
        self.seq_col_name = seq_col_name
    
    def __crete_seq_df(self, df):
        df_seq = df[[self.column]].drop_duplicates()
        df_seq = df_seq.reset_index(drop=True)
        df_seq[self.seq_col_name] = df_seq.index
        return df_seq
    
    def perform(self, df):
        df_seq = self.__crete_seq_df(df)
        return pd.merge(df, df_seq, how='inner', left_on=[self.column], right_on=[self.column])


def check_sequence(values):
    last = -1
    for seq_value in values:
        if last == -1:
            last = seq_value
            assert seq_value == 0
            continue

        assert last == seq_value-1
        last = seq_value