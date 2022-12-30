class Recommendations:
    def __init__(self, metadata, items, info=''):
        self.id          = f'id_{metadata.id}'
        self.title       = metadata.title
        self.description = metadata.description
        self.items       = list(items)
        self.info        = info
        self.position    = metadata.position
        self.metadata    = metadata

    @property
    def empty(self): return len(self.items) == 0


    def __str__(self):
        return str(self.items)


