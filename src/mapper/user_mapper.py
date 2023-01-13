from .mapper import Mapper
from .model  import Model


class UserMapper(Mapper):
    def to_model(self, dto):
        return Model({
            'id': int(dto['id']),
            'username' : dto['username'],
            'email' : dto['email']
        })