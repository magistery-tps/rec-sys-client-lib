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


    def update(self, model):
        dto      = self._mapper.to_dto(model, self._client.host)
        response = self._client.update_similarity_matrix(dto)
        return self._mapper.to_model(response.body[0])


    def versions(self, id: int):
        response = self._client.similarity_matrix_versions(id)
        return [e['version'] for e in response.body]


    def previous_versions(self, id: int):
        versions = self.versions(id)
        versions.sort()
        return versions[:-1]


    def remove_previous_versions(self, id: int):
        previous_versions = self.previous_versions(id)
        [self.remove_version(id, pv) for pv in previous_versions]


    def remove_version(self, id: int, version: int):
        self._client.remove_similarity_version(id, version)


    def remove(id: int): self._client.remove_similarity_matrix(id)
