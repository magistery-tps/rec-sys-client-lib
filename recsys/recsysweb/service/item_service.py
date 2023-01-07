from ..models import Item, Interaction
from django.db import connection
from django.db.models import Q
from singleton_decorator import singleton

class MinMaxScaler:
    def __init__(self, values): self.min_value, self.max_value = min(values), max(values)
    def __call__(self, value): return  (value - self.min_value) / (self.max_value - self.min_value)


@singleton
class ItemService:
    def score_item_by(self, item_id, user, rating):
        item        = Item.objects.get(id=item_id)
        interaction = Interaction.objects.create(
            user   = user.id,
            item   = item,
            rating = rating
        )
        interaction.save()


    def refresh_stats(self):
        items = Item.objects.raw(
            """
                SELECT
                    t.id,
                    t.name,
                    t.description,
                    t.image,
                    avg(t.rating)   as rating,
                    count(*)        as votes,
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


    def find_ids_by_user(self, user):
        return [str(e['item__id']) for e in Interaction.objects.filter(user=user.id).values('item__id')]


    def find_complement_by_tags(self, item_ids, tag_ids, min_popularity = 0):
        return set(
            Item.objects \
                .filter(~Q(pk__in=item_ids)) \
                .filter(
                    tags__id__in   = tag_ids,
                    popularity__gt = min_popularity
                )
        )


    def most_populars(self, limit):
        return Item.objects.all().order_by('popularity')[:limit]


    def unrated_by(self, user, limit):
        return Item.objects.raw(
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
                .replace(':LIMIT', str(limit))
        )
