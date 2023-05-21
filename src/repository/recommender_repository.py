from .entity_repository import EntityRepository
from mapper import RecommenderMapper, Model
import api


class RecommenderRepository(EntityRepository):


    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.RecommenderMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'recommenders')


    def add(self, model: Model):
        """Add a new recommender Model with next structure:

        Examples:
            recommender = Model({
                'id'                     : int,
                'name'                   : str,
                'user_similarity_matrix' : str identifier,
                'item_similarity_matrix' : str identifier
            })

        Args:
            model (Model): Is a dict that represent a recommender model.

        Returns:
            ItemResponse: an ItemResponse object.
        """

        dto      = self._mapper.to_dto(model, self._client.host)
        response = self._client.add_recommender(dto)
        return self._mapper.to_model(response.body[0])


    def update(self, model: Model):
        """Update a recommender Model with next structure:

        Examples:
            recommender = Model({
                'id'                     : int,
                'name'                   : str,
                'user_similarity_matrix' : str identifier,
                'item_similarity_matrix' : str identifier
            })

        Args:
            model (Model): Is a dict that represent a recommender model.

        Returns:
            ItemResponse: an ItemResponse object.
        """

        dto = self._mapper.to_dto(model, self._client.host)
        response = self._client.update_recommender(dto)
        return self._mapper.to_model(response.body[0])


    def remove(id: int):
        """Remove a recommender by identifier

        Args:
            id (int): A recommender identifier.
        """

        self._client.remove_recommender(id)
