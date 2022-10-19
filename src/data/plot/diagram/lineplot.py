import seaborn as sns
import matplotlib.pyplot as plt


def lineplot(
    data,
    x,
    y,
    x_rotation     = 60,
    figsize        = (15, 6),
    title          = '',
    title_fontsize = 20,
    axis_fontsize  = 16
):
    sns.lineplot(x=data[x],  y=data[y].astype('float'))

    sns.set(rc={'figure.figsize': figsize})
    plt.xticks(rotation=x_rotation)
    plt.title(title, fontsize=title_fontsize)
    plt.xlabel(x, fontsize=axis_fontsize)
    plt.ylabel(y, fontsize=axis_fontsize)
    plt.show()

