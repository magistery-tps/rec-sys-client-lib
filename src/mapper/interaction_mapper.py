from .mapper import Mapper


def substring_after(s, delim): return s.partition(delim)[2]


class InteractionMapper(Mapper):
    def to_model(self, dto):
        return {
            'user_id': int(dto['user']),
            'item_id': int(substring_after(dto['item'], 'items/').replace('/', '')),
            'rating' : float(dto['rating'])
        }
