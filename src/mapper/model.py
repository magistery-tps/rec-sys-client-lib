from bunch import Bunch
import api
import util as ut


class Model(Bunch):
    """A DTO object that represent a domain model object.

    Args:
        Bunch (dict): a model state.
    """
    def __init__(self, data): super().__init__(data)
    def __repr__(self): return self.__str__()
    def __str__(self):  return ut.JSON.to_json(self)
