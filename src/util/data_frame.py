from scipy.sparse import  dok_matrix, csr_matrix
import logging
import pandas as pd


norm = lambda df: (df - df.mean()) / df.std()


def df_to_matrix(
    df,
    x_col       = 'user_id',
    y_col       = 'item_id',
    value_col   = 'rating',
    progress    = 10
):
    matrix = dok_matrix((int(df[x_col].max()), int(df[y_col].max())))

    n_examples = df.shape[0]
    count      = 0
    for _, row in df.iterrows():
        matrix[int(row[x_col])-1, int(row[y_col])-1] = float(row[value_col])

        count += 1
        if count % int(n_examples / progress) == 0:
            logging.info(f'Buiding matrix{matrix.shape}... {(count / n_examples) * 100:.0f}%')

    return csr_matrix(matrix)


def concat(df_a, df_b): return pd.concat([df_a, df_b], axis=0)


def save(df, path, header=True): df.to_csv(path, encoding='utf-8', index=False, header=header)


def load(path): return pd.read_csv(path)