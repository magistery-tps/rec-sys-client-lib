class Recommendations:
    def __init__(self, id, name, description, items):
        self.id          = id
        self.name        = name
        self.description = description
        self.items       = list(items)

    @property
    def empty(self): return len(self.items) == 0

    def __str__(self):
        return str(self.items)
