from .mapper import Mapper
from .. import api
from .model  import Model


class RecommenderMapper(Mapper):
    """
    Map a Recommender model to dto and vice versa.
    """

    def to_model(self, dto):
        return Model({
            'id'                     : int(dto['id']),
            'name'                   : str(dto['name']),
            'user_similarity_matrix' : str(dto['user_similarity_matrix']),
            'item_similarity_matrix' : str(dto['item_similarity_matrix'])
        })

    def to_dto(self, model, host=''):
        dto = {
            'name'                   : str(model['name']),
            'user_similarity_matrix' : f'{host}/api/similarity-matrix/{model["user_similarity_matrix"]}/',
            'item_similarity_matrix' : f'{host}/api/similarity-matrix/{model["item_similarity_matrix"]}/'
        }
        if 'id' in model:
            dto['id'] = int(model['id'])
        return dto