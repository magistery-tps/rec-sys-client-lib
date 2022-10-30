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


    def find_items_non_scored_by(self, user, limit = 100):
        return Item.objects.raw(
            """
                SELECT
                    t.item_id as id,
                    t.name,
                    t.description,
                    sum(t.rating) / count(t.rating) as rating
                FROM
                (
                    SELECT 
                        it.id     as item_id,
                        i.user_id as user_id,
                        IF(i.rating IS NULL, 0, i.rating) as rating,
                        it.name   as name,
                        it.description as description,
                        it.image  as image
                    FROM 
                        recsysweb_item AS it 
                        LEFT JOIN 
                        recsysweb_interaction AS i 
                        ON it.id = i.item_id
                ) as t
                WHERE
                    t.item_id NOT IN (
                        SELECT 
                            DISTINCT i.item_id
                        FROM 
                            recsysweb_interaction AS i 
                        WHERE
                            i.user_id = :USER_ID
                    )
                GROUP BY
                    t.item_id
                ORDER BY
                    rating DESC
                LIMIT :LIMIT
            """ \
                .replace('\n', ' ') \
                .replace(':USER_ID', str(user.id)) \
                .replace(':LIMIT', str(limit))
        )


    def find_populars(self, limit=10):
        items = Item.objects.raw(
            """
                SELECT
                    t.item_id as id,
                    t.name,
                    t.description,
                    sum(t.rating) / count(t.rating) as rating
                FROM
                (
                    SELECT 
                        it.id     as item_id,
                        i.user_id as user_id,
                        IF(i.rating IS NULL, 0, i.rating) as rating,
                        it.name   as name,
                        it.description as description,
                        it.image  as image
                    FROM 
                        recsysweb_item AS it  LEFT JOIN 
                        recsysweb_interaction AS i 
                        ON it.id = i.item_id
                ) as t
                GROUP BY t.item_id
                ORDER BY rating DESC
                LIMIT 1000
            """.replace('\n', ' ')
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
            self.find_populars(limit),
            self.find_recommended_for( user, limit)
        ]
        return [ r for r in recs if not r.is_empty()]