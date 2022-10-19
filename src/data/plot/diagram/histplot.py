import seaborn as sns
import matplotlib.pyplot as plt
from ...utils import outliers_range, mode
import numpy as np


def histplot(
    df,
    column,
    bins                 = 'auto',
    stat                 = 'count',
    title                = '',
    title_fontsize       = 16,
    show_mean            = True,
    show_median          = True,
    show_mode            = True,
    show_outliers_leyend = True,
    remove_outliers      = False,
    decimals             = 3
):
    f, (ax_box, ax_hist) = plt.subplots(
        2,
        sharex=True,
        gridspec_kw= {"height_ratios": (0.2, 1)}
    )

    values = df[column].values
    outyliers_lower, outliers_upper = outliers_range(values)

    if remove_outliers:
        values = df[(df[column]>=outyliers_lower) & (df[column]<=outliers_upper)][column].values

    mean       = np.mean(values)
    median     = np.median(values)
    mode_value = mode(values)

    sns.boxplot(x=values, ax=ax_box)
    if show_mean:
        ax_box.axvline(mean,   color='r', linestyle='--')
    if show_median:
        ax_box.axvline(median, color='g', linestyle='-')
    if show_mode:
        ax_box.axvline(mode_value,  color='b', linestyle='-')
    ax_box.set_title(f'Boxplot')
    ax_box.set(xlabel='')

    sns.histplot(x=values, ax=ax_hist, kde=True, bins=bins, stat=stat)

    if show_mean:
        ax_hist.axvline(mean,   color='r', linestyle='--', label=f'Mean ({round(mean, decimals)})')
    if show_median:
        ax_hist.axvline(median, color='g', linestyle='-',  label=f'Mode ({round(median, decimals)})')
    if show_mode:
        ax_hist.axvline(mode_value,   color='b', linestyle='-',  label=f'Mode ({round(mode_value, decimals)})')
    if show_outliers_leyend and not remove_outliers:
        ax_hist.axvline(outyliers_lower,  color='black', linestyle='-', label=f'Outliers lower ({round(outyliers_lower, decimals)})')
        ax_hist.axvline(outliers_upper,   color='black', linestyle='-', label=f'Outliers Upper ({round(outliers_upper, decimals)})')

    ax_hist.legend()

    ax_hist.set_title(f'Histogram')
    ax_hist.set(ylabel='Frequency')
    ax_hist.set(xlabel=column)


    title = f'{title} - {column}' if title else column
    if remove_outliers:
        title  += ' (Without Outliers)'

    f.suptitle(title, fontsize=title_fontsize)

    plt.show()
