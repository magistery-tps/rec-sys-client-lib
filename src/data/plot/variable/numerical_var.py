from ..diagram import histplot


def array_num_to_str(numbers): return [str(n) for n in numbers]


def describe_num_var(
    df,
    column,
    bins                 = 'auto',
    stat                 = 'count',
    title                = '',
    title_fontsize       = 16,
    show_table           = False,
    show_range           = False,
    show_mean            = True,
    show_median          = True,
    show_mode            = True,
    show_outliers_leyend = True,
    remove_outliers      = False,
    decimals             = 3
):
    if show_range or show_table:
        df_column = df[[column]]

    if show_range:
        column_range = (min(df_column.values)[0], max(df_column.values)[0])
        print(f'\nRange: {column_range}\n')

    histplot(
        df,
        column,
        bins,
        stat,
        title,
        title_fontsize,
        show_mean,
        show_median,
        show_mode,
        show_outliers_leyend,
        remove_outliers,
        decimals
    )

    if show_table:
        print('\nMetrics:\n')
        display(df_column.describe())
