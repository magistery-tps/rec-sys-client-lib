from ..models import Item, Interaction, Recommendations
from django.db import connection
import random


class MinMaxScaler:
    def __init__(self, values): self.min_value, self.max_value = min(values), max(values)
    def __call__(self, value): return  (value - self.min_value) / (self.max_value - self.min_value)


class ItemRecService:
    def rate_item_for(self, item_id, user, rating):
        item = Item.objects.get(id=item_id)
        interaction = Interaction.objects.create(
            user   = user.id,
            item   = item,
            rating = rating
        )
        interaction.save()


    def find_items_non_scored_by(self, user):
        return self.find_populars(user, limit=1, shuffle_limit=100)

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
        pop_norm = MinMaxScaler([item.popularity for item  in items])

        for item in items:
            item.popularity = pop_norm(item.popularity)
            item.save()


    def find_populars(self, user, limit=10, shuffle_limit=80):
        items = Item.objects.raw(
            """
                SELECT
                    DISTINCT
                    id,
                    name,
                    description,
					image,
                    popularity
                FROM
                    recsysweb_item
                WHERE
                    id NOT IN (
                        SELECT
                            DISTINCT i.item_id
                        FROM
                            recsysweb_interaction AS i
                        WHERE
                            i.user_id = :USER_ID
                    )
                GROUP BY
                    id
                ORDER BY
                    popularity DESC
                LIMIT :LIMIT
            """ \
                .replace('\n', ' ') \
                .replace(':USER_ID', str(user.id)) \
                .replace(':LIMIT', str(shuffle_limit))
        )

        selected_items = random.choices(items, k=limit)
        selected_items = sorted(selected_items, key=lambda item: item.popularity, reverse=True)

        return Recommendations('populars', selected_items)


    def find_recommended_for(self, user, limit=10):
        return Recommendations(
            name = 'recommended for you',
            items = Item.objects.all()[:limit]
        )


    def find_all(self, user, limit=20):
        recs = [
            self.find_populars(user, limit),
            self.find_recommended_for(user, limit)
        ]
        return [ r for r in recs if not r.is_empty()]