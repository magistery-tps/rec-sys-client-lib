import api
import logging


class EntityRepository:
    def __init__(self, client, mapper, entity): 
        self.__entity = entity
        self.__client = client
        self.__mapper = mapper


    def find(self, filter_fn = lambda dto: True, page_size = 100000):
        iterator = api.ResourceIterator(self.__client, self.__entity, page_size = page_size)        
        models   = []

        for pageDtos in iterator:        
            for itemDto in pageDtos:
                if filter_fn(itemDto):
                    models.append(self.__mapper.to_model(itemDto))
            logging.info(f'- Page {iterator.page}/{iterator.total_pages} - {self.__entity.capitalize()} {iterator.count}/{iterator.total}')

        logging.info(f'- {iterator.total} Total {self.__entity.capitalize()} ')

        return models