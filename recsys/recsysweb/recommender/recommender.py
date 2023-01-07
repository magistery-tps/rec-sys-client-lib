from abc                        import ABC, abstractmethod
from .recommender_context       import RecommenderContext
from .recommender_capability    import RecommenderCapability
from ..models                   import SimilarItemsResult


class Recommender:
    def __init__(self, config):
        self.config = config

    @property
    @abstractmethod
    def metadata(self):
        pass

    @abstractmethod
    def recommend(self, ctx: RecommenderContext):
        pass


    def find_similars(self, ctx: RecommenderContext):
        return SimilarItemsResult(self.metadata)


    @property
    def capabilities(self):
        return [RecommenderCapability.RECOMMEND]
