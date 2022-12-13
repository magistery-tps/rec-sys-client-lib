

class SimilarityCellMapper:

    @staticmethod
    def to_json(
        row     : int,
        column  : int,
        value   : float,
        version : int,
        matrix  : int
    ):
        return {
            'row'   : row,
            'column': column,
            'value' : value,
            'version' : version,
            'matrix': f'http://localhost:8000/api/similarity-matrix/{matrix}/'
        }

    @classmethod
    def data_frame_row_to_json(clz, row):
        return clz.to_json(
            row['row'    ].astype(int),
            row['column' ].astype(int),
            row['value'  ].astype(float),
            row['version'].astype(int),
            row["matrix" ].astype(int)
        )