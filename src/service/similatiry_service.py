import multiprocessing as mp
from itertools import combinations

import numpy as np
import pandas as pd
import tqdm
from logger import get_logger
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingCache:
    def __init__(self, embedding_matrix):
        self.embeddings = {}
        self.embedding_matrix = embedding_matrix

    def __getitem__(self, row_id):
        if row_id not in self.embeddings:
            self.embeddings[row_id] = self.embedding_matrix[row_id].toarray()

        return self.embeddings[row_id]


class SimilarityService:
    def __init__(self):
        self._logger = get_logger(self)

    def similarities(self, embedding_matrix, entity='', n_workers=200, chunks=1_000):
        embeddingCache = EmbeddingCache(embedding_matrix)
        similarities = []

        row_ids = list(range(embedding_matrix.shape[0]))

        # self._logger.info(f'Compute {row_ids}')
        self._logger.info(f'Compute {entity}_seq combinations...')
        row_id_combinations = list(combinations(row_ids, 2))
        self._logger.info(f'{entity}_id combinations...{len(row_id_combinations)} ({len(row_ids)})')

        self._logger.info(f'Compute {entity}_seq embeddings(size: {embedding_matrix.shape[1]})...')
        input_data = []
        for comb in row_id_combinations:
            a_id, b_id = comb[0], comb[1]
            a_emb, b_emb = embeddingCache[a_id], embeddingCache[b_id]
            input_data.append((a_id, b_id, a_emb, b_emb, entity))

        self._logger.info(f'Compute {entity}_id similarities...\n')
        with mp.Pool(processes=n_workers) as pool:
            similarities = [r for r in tqdm.tqdm(pool.imap_unordered(compute_similatiry, input_data, chunks),
                                                 total=len(input_data))]

        return pd.DataFrame(similarities).drop_duplicates()

    def filter_most_similars(self, df, columns, n):
        self._logger.info(f'Filter {n} most similars')

        ids = []
        for column in columns:
            ids.extend(df[column].unique())
        element_ids = np.unique(np.array(ids))

        results = []
        for element_id in element_ids:
            for column in columns:
                most_similares = df[df[column] == element_id] \
                    .sort_values(['value'], ascending=False) \
                    .head(n)
                if most_similares.shape[0] > 0:
                    break

            results.append(most_similares)

        filtered = pd.concat(results)

        self._logger.info(
            f'Filtered: {filtered.shape[0]}/{df.shape[0]} ({(1 - (filtered.shape[0] / df.shape[0])) * 100:.1f}%)')

        return filtered


def compute_similatiry(args):
    (a_id, b_id, a_emb, b_emb, entity) = args
    return {
        f'{entity}_a': a_id,
        f'{entity}_b': b_id,
        'value': cosine_similarity(a_emb, b_emb).flatten()[0]
    }
