import pandas as pd


class XComHelper:
    @classmethod
    def return_value_df(clz, ti, task_id):
        return clz.pull_df(ti, task_id, 'return_value')

    @classmethod
    def return_value(clz, ti, task_id):
        return ti.xcom_pull(key='return_value', task_ids=task_id)

    @staticmethod
    def pull_df(ti, task_id, key):
        json = ti.xcom_pull(key=key, task_ids=task_id)
        return pd.read_json(json)


    @staticmethod
    def push_df(ti, key, df):
        ti.xcom_push(key=key, value=df.to_json())
