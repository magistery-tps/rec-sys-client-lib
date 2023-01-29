from .mapper import Mapper
from .model  import Model


def substring_after(s, delim): return s.partition(delim)[2]


class InteractionMapper(Mapper):
    def to_model(self, dto):
        return Model({
            'user_id': int(dto['user']),
            'item_id': int(substring_after(dto['item'], 'items/').replace('/', '')),
            'rating' : float(dto['rating'])
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