import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging
from sklearn.metrics.pairwise import cosine_similarity
import multiprocessing as mp
from itertools import combinations
import tqdm

class EmbeddingCache:
    def __init__(self, rating_matrix):
        self.embeddings = {}
        self.rating_matrix = rating_matrix

    def __getitem__(self, row_id):
        if row_id not in self.embeddings:
            self.embeddings[row_id] = self.rating_matrix[row_id-1].toarray()

        return self.embeddings[row_id]


class SimilarityService:
    def similarities(self, rating_matrix, row_ids, entity='', n_workers=24, chunks=100_000):
        embeddingCache = EmbeddingCache(rating_matrix)
        similarities = []

        logging.info(f'Compute {entity}_id combinations...')
        row_id_combinations = list(combinations(row_ids, 2))
        logging.info(f'{entity}_id combinations...{len(row_id_combinations)}')

        logging.info(f'Compute {entity}_id embeddings(size: {rating_matrix.shape[1]})...')
        input_data = []
        for comb in row_id_combinations:
            a_id,  b_id  = comb[0], comb[1]
            a_emb, b_emb = embeddingCache[a_id], embeddingCache[b_id]
            input_data.append((a_id, b_id, a_emb, b_emb, entity))

        logging.info(f'Compute {entity}_id similarities...\n')
        with mp.Pool(processes=n_workers) as pool:
            similarities = [r for r in tqdm.tqdm(pool.imap_unordered(compute_similatiry, input_data, chunks), total=len(input_data))]

        return pd.DataFrame(similarities)

    def filter_most_similars(self, df, column, n):
        element_ids = df[column].unique()

        results = []
        for element_id in element_ids:
            most_similares = df[df[column] == element_id] \
                .sort_values([], ascending=False) \
                .head(n)

            results.append(most_similares)

        filtered = pd.concat(results)

        logging.info(f'Filtered: {filtered.shape[0]}/{df.shape[0]} ({(1-(filtered.shape[0]/df.shape[0]))*100:.1f}%)')

        return filtered



def compute_similatiry(args):
    (a_id, b_id, a_emb, b_emb, entity) = args
    return {
        f'{entity}_a': a_id,
        f'{entity}_b': b_id,
        'value': cosine_similarity(a_emb, b_emb).flatten()[0]
    }