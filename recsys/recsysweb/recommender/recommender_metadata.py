class RecommenderMetadata:
    def __init__(self, id, name, title, description, features='', position=0):
        self.id          = id
        self.name        = name
        self.features    = features
        self.title       = f'{title } ({self.features})' if features else title
        self.description = description
        self.position    = position
