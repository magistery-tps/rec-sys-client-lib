from .job import Job
from os.path import exists
from scipy import sparse
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import data as dt
import util as ut


os.environ["TOKENIZERS_PARALLELISM"] = "false"


class BertItemDistanceMatrixJob(Job):
    """This job perform next steps:

    1. Get all user interactions from rec-sys REST API.
    2. Compute all items embeddings from item name and description using a bert model defined into model_name constructor arg.
    3. Build item-item similarity matrix using cosine-similarity.
    4. Create or update matrix from step 3. into rec-sys REST API.

    When it matrix could be used into any rec-sys recommender to perform an similar items recommendation.
    """
    def __init__(
        self,
        ctx,
        model_name,
        n_most_similars = 50
    ):
        """
        Constructor

        Args:
            ctx (DomainContext): a reference to domain context uses to access to all services.
            model_name (str): ber pre-trained model used to genera an embeddings from item name + description.
            n_most_similars (int, optional): Used to filter similarity relations only for n_most_similars of each item. Defaults to 50.
        """
        super().__init__(ctx)
        self.n_most_similars = n_most_similars
        self._job_data_path  = f'{self.ctx.temp_path}/bert_item_{model_name}_job_data'
        self.model           = SentenceTransformer(model_name)
        self.model_name      = model_name


    def _perform(self):
        items = self.ctx.item_service.find_all()

        items = items.rename(columns={'id': 'item_id'})
        items = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(items)

        # Only run when found an interactions size change...
        if exists(f'{self._job_data_path}.pickle'):
            data = ut.Picket.load(self._job_data_path)
            if items.shape[0] == data['n_items']:
                self._logger.info(f'Not found items size change.')
                return
            self._logger.info(f'Fount items size change.')
            self._logger.info(f'Start Computing...')

        # Use item name and description to cumpute embeddings...
        items['description'] = items['name'] + ' ' + items['description']

        data = items[['item_id', 'description']].to_dict()
        data['embedding'] = self.model.encode(data['description'])
        embedding_matrix  = sparse.csr_matrix(np.vstack(data['embedding']))


        item_similarities = self.ctx.similarity_service.similarities(
            embedding_matrix,
            entity='item'
        )

        self.ctx.similarity_matrix_service.update_item_similarity_matrix(
            item_similarities,
            items,
            name            = f'{self.model_name}-item-to-item',
            n_most_similars = self.n_most_similars
        )


        # Save input interactions count...
        ut.Picket.save(self._job_data_path, { 'n_items': items.shape[0] })

