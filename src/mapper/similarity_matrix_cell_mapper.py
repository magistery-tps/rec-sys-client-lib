from .mapper import Mapper
from .model  import Model


class SimilarityMatrixCellMapper(Mapper):
    def to_model(self, dto):
        return Model({
            'id'      : int(dto['id']),
            'row'     : int(dto['row']),
            'column'  : int(dto['colum']),
            'value'   : float(dto['value']),
            'matrix'  : int(dto['matrix']),
            'version' : int(dto['version'])
        })

    def to_dto(self, model, host):
        dto =  {
            'row'     : int(model['row']),
            'column'  : int(model['column' ]),
            'value'   : float(model['value']),
            'version' : int(model['version']),
            'matrix'  : f'{host}/api/similarity-matrix/{model["matrix"]}/'
        }
        if 'id' in model:
            dto['id'] = int(model['id'])
        return dto