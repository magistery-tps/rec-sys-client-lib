import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import util as ut
from sklearn.preprocessing import StandardScaler

def plot_correlations(df, combinations=[]):
    if len(combinations) == 0:
        combinations = ut.combinations(df.columns)

    for colums in combinations:
        colums_ = list(colums)
        correlation_plot(df, colums_[0], colums_[1])


def correlation_plot(
    df,
    column_a,
    column_b,
    title           = '',
    kind            = "line",
    ci              = "sd",
    title_fontsize  = 20,
    figsize         = (11, 9),
    theme_style     = "white"
):
    sns.set_theme(style=theme_style)
    sns.relplot(
        x     = column_a,
        y     = column_b,
        kind  = kind,
        ci    = ci,
        data  = df
    )
    if title == '':
        title = f'Correlación entre {column_a} y {column_b}'
        plt.title(title, fontsize=title_fontsize)

