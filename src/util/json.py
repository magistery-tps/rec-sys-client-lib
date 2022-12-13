from bunch import Bunch
import json



JSON_ENUM_MAPPING = ['SimilarityMatrixType']

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj) if type(obj).__name__ in JSON_ENUM_MAPPING else json.JSONEncoder.default(self, obj)


class JSON:
    @staticmethod
    def to_json(obj, indent=4):
        return json.dumps(obj, indent=indent, cls=EnumEncoder)