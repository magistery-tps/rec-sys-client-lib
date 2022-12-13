from abc import ABCMeta



class Mapper(metaclass=ABCMeta):
    def to_model(self, dto):
        pass

    def to_dto(self, model, host=''):
        pass