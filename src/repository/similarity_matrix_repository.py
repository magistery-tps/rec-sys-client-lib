from .entity_repository import EntityRepository
from mapper import UserMapper
import api


class SimilarityMatrixRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'similarity_matrix')


    def add(
        self,
        name        : str,
        type        : api.SimilarityMatrixType,
        description : str,
        version     : int = 0
    ):
        response = self._client.add_similarity_matrix(name, type, description, version)
        return self._mapper.to_model(response.body[0])


    def update(
        self,
        id          : int,
        name        : str,
        type        : api.SimilarityMatrixType,
        description : str,
        version     : int
    ):
        response = self._client.update_similarity_matrix(id, name, type, description, version)
        return self._mapper.to_model(response.body[0])


    def remove(id: int): self._client.remove_similarity_matrix(id)
