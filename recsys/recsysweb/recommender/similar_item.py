class SimilarItem:
    def __init__(self, item, similarity):
        self.item       = item
        self.similarity = similarity

    @property
    def id(self): return self.item.id

    @property
    def name(self): return self.item.name

    @property
    def description(self): return self.item.description

    @property
    def image(self): return self.item.image

    @property
    def popularity(self): return self.item.popularity

    @property
    def rating(self): return self.item.rating

    @property
    def votes(self): return self.item.votes

    def __str__(self): return f'{str(self.item)} | Similarity: {self.similarity}'
