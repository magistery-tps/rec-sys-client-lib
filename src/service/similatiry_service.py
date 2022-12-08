import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingCache:
    def __init__(self, rating_matrix):
        self.embeddings = {}
        self.rating_matrix = rating_matrix

    def __getitem__(self, row_id):
        if row_id not in self.embeddings:
            self.embeddings[row_id] = self.rating_matrix[row_id-1].toarray()

        return self.embeddings[row_id]


class SimilarityService:
    def similarities(self, rating_matrix, row_ids, progress = 100, entity=''):
        embeddingCache = EmbeddingCache(rating_matrix)
        similarities = []

        total_count = len(row_ids)*len(row_ids)
        count = 0
        for a_id in row_ids:
            a_emb = embeddingCache[a_id]
            for b_id in row_ids:
                b_emb = embeddingCache[b_id]
                similarities.append({
                    f'{entity}_a': a_id,
                    f'{entity}_b': b_id,
                    'value': cosine_similarity(a_emb, b_emb).flatten()[0]
                })
                count += 1
                if count % int(total_count / progress) == 0:
                    logging.info(f'Compute {entity} similarities... {(count / total_count) * 100:.0f}%')

        return pd.DataFrame(similarities)