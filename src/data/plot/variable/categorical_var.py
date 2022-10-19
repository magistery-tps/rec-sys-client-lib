from ..diagram import barplot


def describe_cat_var(
    df,
    column,
    max_shown_values=10,
    order_column=None,
    asc_order=False,
    show_table=False
):
    if order_column == None:
        order_column = 'count'

    count_by_value = df \
    .groupby(column) \
    .size() \
    .reset_index(name='count') \
    .sort_values(by=order_column, ascending=asc_order) \
    .reset_index(drop=True)

    if show_table:
        print(f'\nFrecuency table:\n')
        display(count_by_value)

    barplot(count_by_value, x=column, y='count', title=f'{column} categorical variable')
