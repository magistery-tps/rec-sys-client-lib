class RecommenderMetadata:
    def __init__(self, id, name, title, description, features='', position=0):
        self.id          = id
        self.name        = name
        self.title       = title
        self.features    = features
        self.description = description
        self.position    = position
