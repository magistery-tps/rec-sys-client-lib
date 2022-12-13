from bunch import Bunch
import api
import util as ut


class Model(Bunch):
    def __init__(self, data): super().__init__(data)
    def __repr__(self): return self.__str__()
    def __str__(self):  return ut.JSON.to_json(self)
