import logging

import pandas as pd
import tqdm
from scipy.sparse import dok_matrix, csr_matrix


def seq_by_id(df, entity=None, column_id=None, column_seq=None):
    if entity:
        column_id = f'{entity}_id'
        column_seq = f'{entity}_seq'
    return df_to_dict(df, column_id, column_seq)


def id_by_seq(df, entity=None, column_id=None, column_seq=None):
    if entity:
        column_id = f'{entity}_id'
        column_seq = f'{entity}_seq'
    return df_to_dict(df, column_seq, column_id)


def df_to_dict(df, key_column, value_column):
    """Convert two pd.DataFrame columns to a key-value dict.

    Args:
        df (ps.DataFrame): a data frame.
        key_column (str): key column.
        value_column (str): value column.

    Returns:
        dict[key_column] = value_column: a dict.
    """
    #                  entry.value                  entry.key
    return pd.Series(df[value_column].values, index=df[key_column]).to_dict()


# DF Pipeline functions...

def normalize_column(df, source, target=None):
    if target is None:
        target = source
    df[target] = (df[source] - df[source].mean()) / df[source].std()
    return df


def min_max_scale_column(df, source, target=None):
    if target is None:
        target = source
    df[target] = (df[source] - df[source].min()) / (df[source].max() - df[source].min())
    return df


def apply_fn_to_column(df, target, fn):
    df[target] = fn(df)
    return df


def clean_html_format(df, column):
    import re

    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    def clean_html(raw_html):  return re.sub(CLEANR, '', raw_html) if raw_html else ''

    df[column] = df[column].apply(clean_html)
    return df


def distinct_by(df, columns=[]):
    n_before = df.shape[0]
    df = df.drop_duplicates(subset=columns)
    n_after = df.shape[0]
    logging.info(
        f'Repeated rows by {columns} -> Count: {n_before - n_after}, Percent: {((n_before - n_after) / n_before) * 100:.2f}%')
    return df


def df_to_matrix(
        df,
        x_col,
        y_col,
        value_col='rating'
):
    """Convert a pd.DtaFrame to a 2d space matrix.

    Args:
        df (ps.DataFrame): a pandas data frame.
        x_col (str): column to uses as x axis.
        y_col (str): column to uses as y axis.
        value_col (str, optional): _description_. Defaults to 'rating'.

    Raises:
        IndexError: when ani value into x_col, y_col is out of index range.

    Returns:
        float[int, int]: a sparse matrix.
    """
    logging.info(f'Building matrix({x_col}, {y_col})')

    matrix = dok_matrix((
        len(df[x_col].unique()),
        len(df[y_col].unique())
    ))

    for _, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        try:
            matrix[int(row[x_col]), int(row[y_col])] = float(row[value_col])
        except IndexError as e:
            logging.error(f'Not found index matrix[{int(row[x_col])}, {int(row[y_col])}]')
            raise e

    return csr_matrix(matrix)


def concat(df_a, df_b):
    """Union of two pd.DataFrame objects. Both must have same columns.

    Args:
        df_a (pd.DataFrame): tabla a.
        df_b (pd.DataFrame): table b.

    Returns:
        pd.DataFrame: _description_
    """
    return pd.concat([df_a, df_b], axis=0)


def save(df, path, header=True):
    """SAve a pd.DataFrame to a csv file.

    Args:
        df (pd.DataFrame): table.
        path (str): csv file path.
        header (bool, optional): Include column names. Defaults to True.
    """
    df.to_csv(path, encoding='utf-8', index=False, header=header)


def load(path):
    """Load a pd.DataFrame from a csv file path.

    Args:
        path (str): csv file path.

    Returns:
        pd.DataFrame: table.
    """
    return pd.read_csv(path)
