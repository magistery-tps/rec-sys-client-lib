from os.path import exists

import recsys.data as dt
import recsys.util as ut
import recsys.model as ml

import numpy as np
import logging

from .job import Job


class SurpriseDistanceMatrixJob(Job):
    """This job perform next steps:

    1. Get all user interactions from rec-sys REST API.
    2. Train a model with current user interactions and predict al future interactions.
    3. Build a ratings matrix using current and future interactions.
    4. Build user-item and item-item similarity matrix using cosine-similarity.
    5. Create or update matrix from step 4. into rec-sys REST API.
    """
    def __init__(
            self,
            ctx,
            model,
            recommender_name,
            n_most_similars_users=50,
            n_most_similars_items=10
    ):
        """
        Constructor

        Args:
            ctx (DomainContext): a reference to domain context uses to access to all services.
            model (model.surprise.ModelManager): User to predict future user interactions.
            recommender_name (str): Recommender name associated to user-item and item-item similarity matrix.
            min_item_votes (int, optional): User to filter user with more than min_item_votes interactions. Defaults to 50.
            n_most_similars_users (int, optional): Used to filter similarity relations only for n_most_similars_users of each user. Defaults to 50.
            n_most_similars_items (int, optional): Used to filter similarity relations only for n_most_similars_items of each item. Defaults to 10.
        """
        super().__init__(ctx)
        self._n_most_similars_users = n_most_similars_users
        self._n_most_similars_items = n_most_similars_items
        self._model = model
        self._recommender_name = recommender_name
        self._job_data_path = f'{self.ctx.temp_path}/{self._recommender_name.lower()}_job_data.picket'

    def _perform(self):
        # Get user-item interactions from RecSys API...
        interactions = self.ctx.interaction_service.find_all()

        # Add user/item numeric sequences...
        interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(interactions)
        interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(interactions)

        n_interactions = interactions.shape[0]

        # Only run when found an interactions size change...
        if exists(f'{self._job_data_path}.pickle'):
            data = ut.Picket.load(self._job_data_path)
            if n_interactions == data['n_interactions']:
                self._logger.info(f'Not found interaction size change.')
                return

            self._logger.info(f'Found interactions size change.')
            self._logger.info(f'Start Computing...')

        # Build ratings matrix from user-item interactions..
        future_interactions, train_interactions = self.ctx \
            .interaction_inference_service \
            .predict(
                interactions,
                columns=('user_seq', 'item_seq', 'rating'),
                train_predict_fn   = ml.SurpriseTrainPredictFn(self._model),
                min_n_interactions = 20,
                rating_scale       = np.arange(0, 6, 0.5)
            )

        rating_matrix = self.ctx.rating_matrix_service.create(
            train_interactions,
            future_interactions,
            columns=('user_seq', 'item_seq', 'rating')
        )

        # Build similarity matrix from rating matrix...
        user_similarities, item_similarities = self._build_similarity_matrix(rating_matrix)

        # Update user/item similarity matrix into RecSys API...
        self._upsert_recommender(user_similarities, item_similarities, train_interactions)

        # Save input interactions count...
        ut.Picket.save(self._job_data_path, {'n_interactions': n_interactions})

    def _build_similarity_matrix(self, rating_matrix):
        # Build similarity matrix from rating matrix...
        user_similarities = self.ctx.similarity_service.similarities(
            rating_matrix,
            entity='user'
        )
        item_similarities = self.ctx.similarity_service.similarities(
            rating_matrix.transpose(),
            entity='item'
        )

        return user_similarities, item_similarities

    def _upsert_recommender(self, user_similarities, item_similarities, train_interactions):
        # Update user/item similarity matrix into RecSys API...
        user_similarity_matrix = self.ctx.similarity_matrix_service.update_user_similarity_matrix(
            user_similarities,
            train_interactions,
            name=f'{self._recommender_name}-user-to-user',
            n_most_similars=self._n_most_similars_users
        )
        item_similarity_matrix = self.ctx.similarity_matrix_service.update_item_similarity_matrix(
            item_similarities,
            train_interactions,
            name=f'{self._recommender_name}-item-to-item',
            n_most_similars=self._n_most_similars_items
        )

        # Create or update recommender and asociate with las verison of user/item
        # similarity matrix into RecSys API...
        self.ctx.recommender_service.upsert(
            self._recommender_name,
            user_similarity_matrix,
            item_similarity_matrix
        )
