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

    def to_dto(self, row):
        return {
            'row'     : int(row['row']),
            'column'  : int(row['column' ]),
            'value'   : float(row['value']),
            'version' :  int(row['version']),
            'matrix'  : f'http://localhost:8000/api/similarity-matrix/{int(row["matrix" ])}/'
        }