from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def correlations(
    df,
    title          = 'Diagrama de Correlación',
    title_fontsize = 20,
    figsize        = (11, 9),
    theme_style    = "white"
):
    num_df = df.select_dtypes(include=np.number)

    sns.set_theme(style=theme_style)

    # Compute the correlation matrix
    corr = num_df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=figsize)

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        vmax=.3,
        center=0,
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": .5}
    )
    plt.title(title, fontsize=title_fontsize)
