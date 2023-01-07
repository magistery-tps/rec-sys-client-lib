from ..models import Interaction
from django.db import connection
from bunch import Bunch
from singleton_decorator import singleton


def exec(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


@singleton
class TagService:
    def find_user_profile_by(self, item_ids):
        if len(item_ids) == 0:
            return [], []

        result = exec(
            f'SELECT t.id,t.name,count(item_t.tag_id) FROM recsys.taggit_taggeditem as item_t, recsys.taggit_tag as t WHERE t.id = item_t.tag_id AND item_t.object_id IN ({", ".join(item_ids)}) GROUP BY t.id ORDER BY count(item_t.tag_id) DESC'
        )


        total = sum([row[2] for row in result])
        return (Bunch(id=int(row[0]), name=str(row[1]), score=float(row[2])/total) for row in result)
