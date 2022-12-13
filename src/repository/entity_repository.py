import api
import logging


class EntityRepository:
    def __init__(self, client, mapper, entity):
        self._entity = entity
        self._client = client
        self._mapper = mapper


    def find(self, query={}, page_size = 100000):
        iterator = api.ResourceIterator(
            self._client,
            self._entity,
            page_size = page_size,
            query     = query
        )
        models = []

        for pageDtos in iterator:
            for itemDto in pageDtos:
                models.append(self._mapper.to_model(itemDto))
            logging.info(f'- Page {iterator.page}/{iterator.total_pages} - {self._entity.capitalize()} {iterator.count}/{iterator.total}')

        logging.info(f'- {iterator.total} Total {self._entity.capitalize()} ')

        return models