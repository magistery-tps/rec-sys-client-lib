import api
from logger import get_logger


class EntityRepository:
    def __init__(self, client, mapper, entity):
        self._entity = entity
        self._client = client
        self._mapper = mapper
        self._logger = get_logger(self)


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
            self._logger.info(f'Page {iterator.page}/{iterator.total_pages} - {self._entity.capitalize()} {iterator.count}/{iterator.total}')

        self._logger.info(f'{iterator.total} Total {self._entity.capitalize()} ')

        return models