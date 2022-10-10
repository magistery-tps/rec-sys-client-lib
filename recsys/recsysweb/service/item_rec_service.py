from ..models import Item, Interaction, Recommendations
from django.db import connection


class ItemRecService:
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