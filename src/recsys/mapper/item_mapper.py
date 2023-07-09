from .mapper import Mapper
from .model  import Model


class ItemMapper(Mapper):
    """
    Map a Item model to dto and vice versa.
    """

    def to_model(self, dto):
        return Model({
            'id'         : int(dto['id']),
            'name'       : str(dto['name']),
            'description': str(dto['description']),
            'popularity' : float(dto['popularity']),
            'rating'     : float(dto['rating']),
            'votes'      : int(dto['votes']),
            'tags'       : dto['tags']
        })
