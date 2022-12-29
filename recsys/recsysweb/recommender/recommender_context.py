class RecommenderContext:
    def __init__(self, user=None, limit=20, shuffle_limit=80, item=None):
        self.user          = user
        self.limit         = limit
        self.shuffle_limit = shuffle_limit
        self.item          = item
