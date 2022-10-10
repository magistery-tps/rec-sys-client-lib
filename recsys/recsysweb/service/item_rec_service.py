from ..models import Item, Interaction, Recommendations
from django.db import connection


class ItemRecService:
    def rate_item_for(self, item_id, user, rating):
        item = Item.objects.get(id=item_id)
        interaction = Interaction.objects.create(
            user   = user,
            item   = item,
            rating = rating
        )
        interaction.save()


    def find_unrated_by(self, user):
        return Item.objects.raw(
            f'SELECT it.id FROM recsys.recsysweb_item AS it LEFT JOIN recsys.recsysweb_interaction AS i ON it.id = i.item_id AND i.user_id != {user.id} ORDER BY i.rating DESC LIMIT 1'
        )


    def find_populars(self, limit=10):
        return Recommendations(
            name = 'populars',
            items = Item.objects.all()[:limit]
        )


    def find_recommended_for(self, user, limit=10):
        return Recommendations(
            name = 'recommended for you', 
            items = Item.objects.all()[:limit]
        )


    def find_all(self, user, limit=10):
        recs = [
            self.find_populars(limit),
            self.find_recommended_for( user, limit)
        ]
        return [ r for r in recs if not r.is_empty()]