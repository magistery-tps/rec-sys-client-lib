from ..diagram import words_clous_plot
from ...utils import outliers_range


def describe_text_var(df, column, flatten=False):
    values = df[column].values.tolist()

    if flatten:
        values = [vv for v in values for vv in v]

    words_clous_plot(values, title = f'{column} text variable')