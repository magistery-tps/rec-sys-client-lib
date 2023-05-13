import data as dt
import util as ut
from .job import Job


class RecommenderValidationJob(Job):
    def __init__(
        self,
        ctx,
        model,
        n_most_similars_users = 50,
        n_most_similars_items = 10
    ):
        super().__init__(ctx)
        self._n_most_similars_users = n_most_similars_users
        self._n_most_similars_items = n_most_similars_items
        self._model                 = model

    def _perform(self):
        # Get user-item interacitons from RecSys API...
        interactions = self.ctx.interaction_service.find_all()

        # Add user/item numeric sequences...
        interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(interactions)
        interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(interactions)


        # Build ratings matrix from user-item interactions..
        rating_matrix, train_interactions = self.ctx.rating_matrix_service.create(
            interactions,
            columns = ('user_seq', 'item_seq', 'rating'),
            model   = self._model
        )

        # Build similarity matrix from rating matrix...
        user_similarities, item_similarities = self._build_similatrity_matrix(rating_matrix)


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

        return user_similarities, item_similarities

