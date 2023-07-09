from .entity_repository import EntityRepository
from recsys.mapper import UserMapper
from .. import api


class SimilarityMatrixRepository(EntityRepository):


    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.SimilarityMatrixMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'similarity_matrix')


    def add(
        self,
        name        : str,
        type        : api.SimilarityMatrixType,
        description : str,
        version     : int = 0
    ):
        """Create a similarity matrix.

        Args:
            name (str): Similarity matrix name.
            type (api.SimilarityMatrixType): Type of similarity matrix.
            description (str): A description.
            version (int, optional): A similarity matrix initial version. Defaults to 0.

        Returns:
            Model: A similarity matrix model.
        """
        response = self._client.add_similarity_matrix(name, type, description, version)
        return self._mapper.to_model(response.body[0])


    def update(self, model):
        """Update a similarity matrix Model with next structure:

        similarity_matrix = Model({\n
            'id'         : int,\n
            'name'       : str,\n
            'type'       : api.SimilarityMatrixType [USER_TO_USER, ITEM_TO_ITEM],\n
            'description': str,\n
            'version'    : int\n
        })

        Args:
            model (Model): Is a dict that represent a similarity matrix model.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        dto      = self._mapper.to_dto(model, self._client.host)
        response = self._client.update_similarity_matrix(dto)
        return self._mapper.to_model(response.body[0])


    def versions(self, id: int):
        """
        Query versions of a given similarity matrix.

        Args:
            id (int): A similarity matrix identifier.

        Returns:
            list: a list of int versions.
        """
        response = self._client.similarity_matrix_versions(id)
        return [e['version'] for e in response.body]


    def previous_versions(self, id: int):
        """
        Query previous versions of a given similarity matrix.

        Args:
            id (int): A similarity matrix identifier.

        Returns:
            list: a list of int versions.
        """
        versions = self.versions(id)
        versions.sort()
        return versions[:-1]


    def remove_previous_versions(self, id: int):
        """Remove a previous similar matrix cell version by identifier.

        Args:
            id (int): A similar matrix cell identifier.
            version (int): A previous similar matrix cell version number.
        """
        previous_versions = self.previous_versions(id)
        [self.remove_version(id, pv) for pv in previous_versions]


    def remove_version(self, id: int, version: int):
        """Remove a similar matrix cell version by identifier.

        Args:
            id (int): A similar matrix cell identifier.
            version (int): A similar matrix cell version number.
        """
        self._client.remove_similarity_version(id, version)


    def remove(id: int):
        """Remove a similar matrix cell by identifier.

        Args:
            id (int): A similar matrix cell identifier.
        """
        self._client.remove_similarity_matrix(id)
