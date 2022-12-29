from abc import ABC, abstractmethod
from .recommender_context import RecommenderContext


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