class RecommenderMetadata:
    def __init__(self, id, name, title, description, features='', position=0, shuffle=False, active_nested_metadata=None, n_items_by_session=None):
        self.id                     = id
        self.name                   = name
        self.title                  = title
        self.features               = features
        self.description            = description
        self.position               = position
        self.shuffle                = shuffle
        self.active_nested_metadata = active_nested_metadata
        self.n_items_by_session     = n_items_by_session