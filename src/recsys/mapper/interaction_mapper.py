from .mapper import Mapper
from .model  import Model
from datetime import datetime


DEFAULT_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def str_to_datetime(value, format=DEFAULT_DATE_TIME_FORMAT):
    return datetime.strptime(value, format)

def substring_after(s, delim): return s.partition(delim)[2]


class InteractionMapper(Mapper):
    """
    Map a Interaction model to dto and vice versa.
    """
    def to_model(self, dto):
        return Model({
            'user_id'           : int(dto['user']),
            'item_id'           : int(substring_after(dto['item'], 'items/').replace('/', '')),
            'rating'            : float(dto['rating']),
            'suitable_to_train' : bool(dto['suitable_to_train']),
            'created_at'        : str_to_datetime(dto['created_at'])
        })


    def to_dto(self, model, host):
        dto =  {
            'user'              : int(model['user_id']),
            'item'              : f'{host}/api/items/{model["item_id"]}/',
            'rating'            : float(model['rating']),
            'suitable_to_train' : bool(model['suitable_to_train'])
        }

        if 'id' in model:
            dto['id'] = int(model['id'])
        return dto
