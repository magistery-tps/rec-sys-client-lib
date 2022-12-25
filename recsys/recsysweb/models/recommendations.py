class Recommendations:
    def __init__(self, id, name, description, items, not_found='Not found recommendations!'):
        self.id          = id
        self.name        = name
        self.description = description
        self.items       = list(items)
        self.not_found   = not_found

    @property
    def empty(self): return len(self.items) == 0

    def __str__(self):
        return str(self.items)
