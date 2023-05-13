from ..models import Item, Interaction
from django.db import connection
from django.db.models import Q
from singleton_decorator import singleton
from django.core.paginator import Paginator
from django.conf import settings
from ..logger import get_logger
import pickle


class MinMaxScaler:
    def __init__(self, values): self.min_value, self.max_value = min(values), max(values)
    def __call__(self, value): return  (value - self.min_value) / (self.max_value - self.min_value)


def load(path):
    with open(f'{path}.pickle', 'rb') as handle:
        return pickle.load(handle)


@singleton
class ItemService:
    def __init__(self):
        self.logger = get_logger(self)


    def find_paginated(self, tags=[], page_number=0, page_size=settings.ITEMS_PAGE_SIZE):
        items     = self.find_by_tags(tags)
        paginator = Paginator(items, page_size)
        return paginator.get_page(page_number)


    def find_by_tags(self, tags=[]):
        tags = [tag.replace('"', '').replace("'", '') for tag in tags]

        positive_tags = [t for t in tags if '-' not in t]
        negative_tags = [t.replace('-', '') for t in tags if '-' in t]

        items = Item.objects

        if tags:
            if positive_tags:
                self.logger.info(f'Tags - Positive: {positive_tags}')
                for pos_tag in positive_tags:
                    items = items.filter(tags__name__in=[pos_tag])

            if negative_tags:
                self.logger.info(f'Tags - Negative: {negative_tags}')
                for neg_tag in negative_tags:
                    items = items.exclude(tags__name__in=[neg_tag])
        else:
            items = items.all()

        return items

    def find_by_id(self, id):
        return Item.objects.get(id=id)


    def score_items_by(self, user, items_rating):
        ratings = list(filter(lambda it: it>0, items_rating.keys()))

        for item in Item.objects.filter(id__in=ratings):
            interaction = Interaction.objects.create(
                user   = user.id,
                item   = item,
                rating = items_rating[item.id]
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
        return Item.objects.all().order_by('-popularity')[:limit]


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

    
    def add_tags_from(self, path):
        filtered_items = [(name, tags) for (name, tags) in load(path).items() if len(tags) > 0]

        self.logger.info(f'Item with tags: {len(filtered_items)}')

        for (id, tags) in filtered_items:
            result = Item.objects.filter(id=id)
            if len(result) > 0:
                item = result[0]
                self.logger.info(f'Item: {item}, Tags: {tags}')
                for tag in tags:
                    item.tags.add(tag)


