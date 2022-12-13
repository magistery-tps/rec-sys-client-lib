from .entity_repository import EntityRepository
from mapper import RecommenderMapper, Model
import api


class RecommenderRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'recommenders')


    def add(self, model: Model):
        dto      = self._mapper.to_dto(model, self._client.host)
        response = self._client.add_recommender(dto)
        return self._mapper.to_model(response.body[0])


    def update(self, model: Model):
        dto = self._mapper.to_dto(model, self._client.host)
        response = self._client.update_recommender(dto)
        return self._mapper.to_model(response.body[0])


    def remove(id: int): self._client.remove_recommender(id)
