from airflow.models import TaskInstance

class EnhancedTaskContext:
    def __init__(self, ctx):
        self.__ctx = ctx

    @property
    def dag_instance(self):
        return self.__ctx['dag']

    @property
    def task_instance(self):
        operator_instance = self.dag_instance.get_task(ctx['task_id'])

        return TaskInstance(operator_instance).current_state()

    @property
    def previous_task_id(self):
        return next(iter(self.__ctx['task'].upstream_task_ids))

    def __getitem__(self, key):
         return self.__ctx[key]