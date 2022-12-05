from scipy.sparse import  dok_matrix, csr_matrix
import logging
from IPython.display import clear_output


norm = lambda df: (df - df.mean()) / df.std()


def df_to_matrix(df, x_col='user_id', y_col='item_id', value_col='rating', progress_each = 100000):
    matrix =  dok_matrix((
        int(df[x_col].max()),
        int(df[y_col].max())
    ))

    count = 0
    for _, row in df.iterrows():
        matrix[int(row[x_col])-1, int(row[y_col])-1] = float(row[value_col])
        count += 1
        if count % progress_each == 0:
            clear_output(wait=True)
            percent = (count / df.shape[0]) * 100
            logging.info(f'Processing: {percent:.0f}%')

    return csr_matrix(matrix)