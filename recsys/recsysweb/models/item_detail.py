class ItemDetail:
    def __init__(self, item, similar_items, recommender):
        self.item           = item
        self.similars_title = f'Similars ({recommender.metadata.name} Recommender)'
        self.similar_items  = similar_items
        self.metadata       = recommender.metadata