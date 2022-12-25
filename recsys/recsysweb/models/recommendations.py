class Recommendations:
    def __init__(self, name, description, items):
        self.id          = name.replace(' ', '-')
        self.name        = name
        self.description = description
        self.items       = list(items)

    @property
    def empty(self): return len(self.items) == 0

    def __str__(self):
        return str(self.items)
