from .mapper import Mapper
from .model  import Model
import re


class SimilarityMatrixCellMapper(Mapper):
    """
    Map a SimilarityMatrixCell model to dto and vice versa.
    """

    def to_model(self, dto):
        
        
        dto['matrix']
        
        return Model({
            'id'      : int(dto['id']),
            'row'     : int(dto['row']),
            'column'  : int(dto['column']),
            'value'   : float(dto['value']),
            'matrix'  : self._get_assocaition_id(dto['matrix']),
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
    
    
    def _get_assocaition_id(self, value):
        return value.split('/')[-2]