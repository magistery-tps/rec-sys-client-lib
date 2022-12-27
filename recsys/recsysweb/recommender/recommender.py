from abc import ABC, abstractmethod


class RecommenderContext:
    def __init__(self, user=None, limit=20, shuffle_limit=80):
        self.user          = user
        self.limit         = limit
        self.shuffle_limit = shuffle_limit


class Recommender:
    @abstractmethod
    def recommend(self, ctx: RecommenderContext):
        pass