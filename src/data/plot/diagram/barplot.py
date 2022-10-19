import seaborn as sns
import matplotlib.pyplot as plt


def barplot(
    data,
    x,
    y,
    title          = '',
    title_fontsize = 20,
    axis_fontsize  = 16,
    x_rotation     = 60,
    figsize        = (15, 6)
):
    sns.barplot(x=data[x],  y=data[y].astype('float'))

    plt.xticks(rotation=x_rotation)
    sns.set(rc={'figure.figsize': figsize})
    plt.title(title, fontsize=title_fontsize)
    plt.xlabel(x, fontsize=axis_fontsize)
    plt.ylabel(y, fontsize=axis_fontsize)
    plt.show()
