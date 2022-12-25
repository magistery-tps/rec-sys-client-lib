from surprise import SVD
import data as dt
import util as ut
from .job import Job
from os.path import exists


class SurpriseDistanceMatrixJob(Job):
    def __init__(
        self,
        ctx,
        model                 = SVD(),
        recommender_name      = 'SVD',
        n_most_similars_users = 500,
        n_most_similars_items = 500,
        n_interactions_delta  = 50
    ):
        super().__init__(ctx)
        self._n_most_similars_users = n_most_similars_users
        self._n_most_similars_items = n_most_similars_items
        self._model                 = model
        self._recommender_name      = recommender_name
        self._n_interactions_delta  = n_interactions_delta
        self._job_data_path         = f'{self.ctx.temp_path}/{self._recommender_name.lower()}_job_data'

    def _perform(self):
        # Get user-item interacitons from RecSys API...
        interactions = self.ctx.interaction_service.find_all()

        # Add user/item numeric sequences...
        interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(interactions)
        interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(interactions)

        n_interactions = interactions.shape[0]

        # self._logger.info(f'5000 USER_ID INTERACTIONS: {interactions[interactions["user_id"] == 5000].shape}')


        # Only run when found more than n_interactions_delta new interactions...
        if exists(f'{self._job_data_path}.pickle'):
            data = ut.Picket.load(self._job_data_path)
            if (data['n_interactions'] + self._n_interactions_delta) >= n_interactions:
                self._logger.info(f'Unreached minimum new interactions threshold({self._n_interactions_delta}).')
                return
            self._logger.info(f'Reached minimum new interactions threshold({self._n_interactions_delta}).')
            self._logger.info(f'Start Computing...')


        # Build ratings matrix from user-item interactions..
        rating_matrix, train_interactions = self.ctx.rating_matrix_service.create(
            interactions,
            columns = ('user_seq', 'item_seq', 'rating'),
            model   = self._model
        )


        # user_seq = train_interactions[train_interactions["user_id"] == 5000]["user_seq"].unique()
        # self._logger.info(f'5000 USER_SEQ: {user_seq}')
        # self._logger.info(f'5000 USER_ID INTERACTIONS: {train_interactions[train_interactions["user_id"] == 5000].shape}')

        # user_seqs = train_interactions["user_seq"].unique()
        # user_seqs.sort()
        # self._logger.info(f'TRAIN USER_SEQS: {user_seqs}')

        # Build similarity matrix from rating matrix...
        user_similarities, item_similarities = self._build_similatrity_matrix(rating_matrix)


        # user_seqs = user_similarities["user_a"].unique()
        # user_seqs.sort()
        # self._logger.info(f'USER_SEQS A: {user_seqs}')

        # user_seqs = user_similarities["user_b"].unique()
        # user_seqs.sort()
        # self._logger.info(f'USER_SEQS B: {user_seqs}')

        # Update user/item similarity matrix into RecSys API...
        self._upsert_recommender(user_similarities, item_similarities, train_interactions)


        # Save input interactions count...
        ut.Picket.save(self._job_data_path, { 'n_interactions': n_interactions })



    def _build_similatrity_matrix(self, rating_matrix):
        # Build similarity matrix from rating matrix...
        user_similarities = self.ctx.similarity_service.similarities(
            rating_matrix,
            entity = 'user'
        )
        item_similarities = self.ctx.similarity_service.similarities(
            rating_matrix.transpose(),
            entity = 'item'
        )

        # user_similarities = user_similarities[user_similarities['value'] > 0.0]
        # item_similarities = item_similarities[item_similarities['value'] > 0.0]
        return user_similarities, item_similarities


    def _upsert_recommender(self, user_similarities, item_similarities, interactions):
        # Update user/item similarity matrix into RecSys API...
        user_similarity_matrix = self.ctx.similarity_matrix_service.update_user_similarity_matrix(
            user_similarities,
            interactions,
            name            = f'{self._recommender_name}-user-to-user',
            n_most_similars = self._n_most_similars_users
        )
        item_similarity_matrix = self.ctx.similarity_matrix_service.update_item_similarity_matrix(
            item_similarities,
            interactions,
            name            = f'{self._recommender_name}-item-to-item',
            n_most_similars = self._n_most_similars_items
        )


        # Create or update recommender and asociate with las verison of user/item
        # similarity matrix into RecSys API...
        self.ctx.recommender_service.upsert(
            self._recommender_name,
            user_similarity_matrix,
            item_similarity_matrix
        )
