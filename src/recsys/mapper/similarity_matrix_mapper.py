from .mapper import Mapper
from .. import api
from .model  import Model


class SimilarityMatrixMapper(Mapper):
    """
    Map a SimilarityMatrix model to dto and vice versa.
    """

    def to_model(self, dto):
        return Model({
            'id'         : int(dto['id']),
            'name'       : str(dto['name']),
            'type'       : api.SimilarityMatrixType(dto['type']),
            'description': str(dto['description']),
            'version'    : int(dto['version'])
        })

    def to_dto(self, model, host=''):
        dto = {
            'name'        : str(model['name']),
            'type'        : int(model['type'].value),
            'description' : str(model['description']),
            'version'     : int(model['version'])
        }
        if 'id' in model:
            dto['id'] = int(model['id'])
        return dto