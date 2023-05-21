import api
from logger import get_logger


class EntityRepository:
    def __init__(self, client, mapper, entity):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.RecommenderMapper): mapper to map objects between dto-model.
            entity (str): api resource name of entity in lower case.
        """
        self._entity = entity
        self._client = client
        self._mapper = mapper
        self._logger = get_logger(self)


    def find(self, query={}, page_size = 100000):
        """
        Allows to query entities by ani entity field.

        Args:
            query (dict, optional): A dict of field_name: value pairs. Defaults to {}.
            page_size (int, optional): Page size. Defaults to 100000.

        Returns:
            a dict list: A lost of dict. Each dist represent an entity or model like an interaction, a similar matrix, etc...
        """
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