class Recommendations:
    def __init__(self, id, name, description, items, position=0, info=''):
        self.id          = f'id_{id}'
        self.name        = name
        self.description = description
        self.items       = list(items)
        self.info        = info
        self.position    = position

    @property
    def empty(self): return len(self.items) == 0

    def __str__(self):
        return str(self.items)
