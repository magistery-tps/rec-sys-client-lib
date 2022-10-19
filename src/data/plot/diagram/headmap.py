import seaborn as sns
import matplotlib.pyplot as plt


def headmap(
    matrix,
    title          = '',
    figsize        = (10, 10),
    hide_labels    = True,
    title_fontsize = 20
):
    sns.heatmap(matrix, xticklabels=not hide_labels, yticklabels=not hide_labels)

    sns.set(rc={'figure.figsize': figsize})
    plt.title(title, fontsize=title_fontsize)
    plt.show()