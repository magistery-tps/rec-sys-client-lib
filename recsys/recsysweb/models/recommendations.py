class Recommendations:
    def __init__(self, name, items):
        self.name  = name
        self.id    = name.replace(' ', '-')
        self.items = list(items)

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return str(self.items)
