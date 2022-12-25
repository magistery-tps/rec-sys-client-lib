from ..models import Item, Interaction
from django.db import connection
import random


class MinMaxScaler:
    def __init__(self, values): self.min_value, self.max_value = min(values), max(values)
    def __call__(self, value): return  (value - self.min_value) / (self.max_value - self.min_value)


class ItemService:
    def score_item_by(self, item_id, user, rating):
        item        = Item.objects.get(id=item_id)
        interaction = Interaction.objects.create(
            user   = user.id,
            item   = item,
            rating = rating
        )
        interaction.save()


    def refresh_popularity(self):
        items = Item.objects.raw(
            """
                SELECT
                    t.id,
                    t.name,
                    t.description,
                    t.image,
                    ( avg(t.rating) * (COUNT(*)/(SELECT COUNT(*) FROM recsys.recsysweb_interaction)) ) as popularity
                FROM
                    (
                        SELECT
                            it.id,
                            it.name,
                            it.description,
                            it.image,
                            inter.rating
                        FROM
                                recsys.recsysweb_item AS it
                            INNER JOIN
                                recsys.recsysweb_interaction AS inter
                            ON
                                it.id = inter.item_id
                    ) as t
                GROUP BY
                    t.id
            """
        )
        popularity_normalizer = MinMaxScaler([item.popularity for item  in items])

        for item in items:
            item.popularity = popularity_normalizer(item.popularity)
            item.save()



    def find_all(self, user, limit=20):
        recs = [
            self.find_non_seen_populars(user, limit),
            self.find_recommended_for(user, limit)
        ]
        return [ r for r in recs if not r.is_empty()]