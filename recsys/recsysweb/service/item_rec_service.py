from ..models import Item, Interaction, Recommendations
from django.db import connection
import random


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
        return self.find_populars(user, limit=1, shuffle_limit=1)


    def refresh_popularity(self):
        items = Item.objects.raw(
            """
                SELECT
                    t.item_id as id,
                    t.name,
                    t.description,
					t.image,
                    (count(t.rating)/ (SELECT COUNT(*) FROM recsysweb_interaction)) * avg(t.rating) * 10000 as popularity
                FROM
                (
                    SELECT
                        it.id          as item_id,
                        inter.user_id  as user_id,
                        IF(inter.rating IS NULL, 0, inter.rating) as rating,
                        it.name        as name,
                        it.description as description,
                        it.image       as image
                    FROM
						recsysweb_item AS it INNER JOIN recsysweb_interaction AS inter
                        ON it.id = inter.item_id
                ) as t
                GROUP BY
					t.item_id
            """
        )
        for item in items:
            item.save()


    def find_populars(self, user, limit=10, shuffle_limit=100):
        items = Item.objects.raw(
            """
                SELECT
                    *
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

        return Recommendations(
            name = 'populars',
            items = random.choices(items, k=limit)
        )


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