from abc import ABC, abstractmethod


class RecommenderMetadata:
    def __init__(self, id, name, description, position=0):
        self.id          = id
        self.name        = name
        self.description = description
        self.position    = position


class RecommenderContext:
    def __init__(self, user=None, limit=20, shuffle_limit=80, item=None):
        self.user          = user
        self.limit         = limit
        self.shuffle_limit = shuffle_limit
        self.item          = item


class Recommender:
    @property
    @abstractmethod
    def metadata(self):
        pass

    @abstractmethod
    def recommend(self, ctx: RecommenderContext):
        pass


    @abstractmethod
    def find_similars(self, ctx: RecommenderContext):
        pass