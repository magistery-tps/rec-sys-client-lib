from .mapper import Mapper
import api
from .model  import Model


class SimilarityMatrixMapper(Mapper):
    def to_model(self, dto):
        return Model({
            'id'         : int(dto['id']),
            'name'       : str(dto['name']),
            'type'       : api.SimilarityMatrixType(dto['type']),
            'description': str(dto['description']),
            'version'    : int(dto['version'])
        })

    def to_dto(self, model):
        return {
            'name'        : str(model['name']),
            'type'        : int(model['type'].value),
            'description' : str(model['description']),
            'version'     : int(model['version'])
        }