from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from sklearn.utils import Bunch
from enum import Enum
import bunch
import json
import pandas as pd


class ListResponse:
    """
    An object that represent an api response. This contains an status(http code), body, and results properties.

    results represent a list of items. Used to query a list of instance for a give REST Result list interactions, users, etc..
    """
    def __init__(self, status, body):
        self.status = status
        self.body   = bunch.Bunch(body)
        if 'results' in body:
            self.body.results = [bunch.Bunch(item) for item in self.body.results]


    def __repr__(self): return self.__str__()


    def __str__(self):  return json.dumps({'status': self.status, 'body': self.body}, indent=4)


class ItemResponse:
    """
    An object that represent an api response. this contains an status(http code) and a response body properties.
    """
    def __init__(self, status, body):
        self.status = status
        if type(body) == list:
            self.body = [bunch.Bunch(item) for item in body]
        else:
            self.body = [body]


    def __repr__(self): return self.__str__()


    def __str__(self):  return json.dumps({'status': self.status, 'body': self.body}, indent=4)


class ActionsFactory:
    @staticmethod
    def create(name, filters='', extra_actions={}):
        actions = {
            'pages':  { 'method': 'GET',    'url': "/api/" + name + "/?offset={}&limit={}" + filters },
            'add':    { 'method': 'POST',   'url': "/api/" + name + "/" },
            'update': { 'method': 'PUT',    'url': "/api/" + name + "/{}/" },
            'remove': { 'method': 'DELETE', 'url': "/api/" + name + "/{}/" }
        }
        return actions | extra_actions


class SimilarityMatrixType(Enum):
    USER_TO_USER = 1
    ITEM_TO_ITEM = 2


class UserResource(Resource):
    actions = ActionsFactory.create(
        name    = 'users',
        filters = '&username={}&email={}'
    )


class ItemResource(Resource):
    actions = ActionsFactory.create(
        name    = 'items',
        filters = '&name={}&description={}{}'
    )


class InteractionResource(Resource):
    actions = ActionsFactory.create(
        name     = 'interactions',
        filters  = '&user={}&item={}'
    )


class SimilarityMatrixResource(Resource):
    actions = ActionsFactory.create(
        name    = 'similarity-matrix',
        filters = '&name={}&type={}&description={}&version={}',
        extra_actions = {
            'versions'       : { 'method': 'GET',    'url': '/api/similarity-matrix/{}/versions/' },
            'remove_version' : { 'method': 'DELETE', 'url': '/api/similarity-matrix/{}/versions/{}/' }
        }
    )


class SimilarityMatrixCellResource(Resource):
    actions = ActionsFactory.create(
        name          = 'similarity-matrix-cells',
        filters       = '&row={}&column={}&matrix={}'
    )


class RecommenderResource(Resource):
    actions = ActionsFactory.create('recommenders', '&name={}')


"""
https://python-simple-rest-client.readthedocs.io/en/latest/quickstart.html
"""
class RecSysApi:
    """
    rec-sys REST API client. Used to interact with rec-sys services.
    """
    def __init__(self, token, host='http://localhost:8000', timeout=500):
        """

        Create rec-sys REST API client.

        Args:
            token (str): required to access to api end-points.
            host (str, optional): base rec-sys service utl. Defaults to 'http://localhost:8000'.
            timeout (int, optional): Request timeout. Defaults to 500.
        """
        headers = {'Authorization': f'Token {token}'}
        api = API(
            api_root_url     = host,
            headers          = headers,
            json_encode_body = True,
            timeout          = timeout
        )
        api.add_resource(
            resource_name  = 'users',
            resource_class = UserResource
        )
        api.add_resource(
            resource_name  = 'items',
            resource_class = ItemResource
        )
        api.add_resource(
            resource_name  = 'interactions',
            resource_class = InteractionResource
        )
        api.add_resource(
            resource_name  = 'similarity_matrix',
            resource_class = SimilarityMatrixResource
        )
        api.add_resource(
            resource_name  = 'similarity_matrix_cell',
            resource_class = SimilarityMatrixCellResource
        )
        api.add_resource(
            resource_name  = 'recommenders',
            resource_class = RecommenderResource
        )
        self.api  = api
        self.host = host


    def _resp(self, response):
        return ItemResponse(response.status_code, response.body)


    def _list_resp(self, response):
        return ListResponse(response.status_code, response.body)


    # Users
    def users(self, offset=0, limit=10, username='', email=''):
        return self._list_resp(self.api.users.pages(
            offset, limit, username, email
        ))


    # Items
    def items(self, offset=0, limit=10, name='', description='', tags=[]):
        tags_uri = '&' + '&'.join([f'tag={tag}'for tag in tags]) if tags else ''

        return self._list_resp(self.api.items.pages(
            offset, limit, name, description, tags_uri
        ))
    #--------------------------------------------------------------------------
    #
    #
    #
    #--------------------------------------------------------------------------
    # Interactions
    #--------------------------------------------------------------------------
    def bulk_add_interactions(self, body):
        """
        Add new user interactions in bulk way. An interaction is must be represented by a dict:

        Examples:
            interaction = {
                'user'              : int,
                'item'              : int,
                'rating'            : float,
                'suitable_to_train' : bool
            }

        Args:
            body (an interactions list): A list of dicts. Each dist represent an interaction dto.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.interactions.add(body=body))


    def interactions(self, offset=0, limit=10, user='', item=''):
        """
        Query user interactions. An interaction is a dict dto with next structure:

        interaction = {
            'user'              : int,
            'item'              : int,
            'rating'            : float,
            'suitable_to_train' : bool
        }

        It method also allow as to query using pagination an also filter by user id and/or item id.

        Args:
            offset (int, optional): Page start from offset. Defaults to 0.
            limit (int, optional): Page size. Defaults to 10.
            user (str, optional): User identifier. Defaults to ''.
            item (str, optional): Item identifier. Defaults to ''.

        Returns:
            ListResponse: a ListResponse instance.
        """
        return self._list_resp(self.api.interactions.pages(
            offset, limit, user, item
        ))
    #--------------------------------------------------------------------------
    #
    #
    #
    #--------------------------------------------------------------------------
    # Similarity Matrix
    #--------------------------------------------------------------------------
    def similarity_matrix(
        self,
        offset      : int = 0,
        limit       : int = 10,
        name        : str = '',
        type        : str = '',
        description : str = '',
        version     : str = ''
    ):
        """
        Query a similarity matrix. An interaction is a dict dto with next structure:

        Examples:
            similarity_matrix = {
                'name'        : str,
                'type'        : int [USER_TO_USER = 1, ITEM_TO_ITEM = 2],
                'description' : str,
                'version'     : int
            }

        It method also allow as to query using pagination an also filter by name, type, description, version.

        Args:
            offset (int, optional): Page start from offset. Defaults to 0.
            limit (int, optional): Page size. Defaults to 10.
            name (str, optional): Similarity matrix name. Defaults to ''.
            type (str, optional): Similarity matrix type: 1 is USER_TO_USER. 2 is ITEM_TO_ITEM. Defaults to ''
            description (str, optional): Similarity matrix description. Defaults to ''.
            version (str, optional): Similarity matrix version. Defaults to ''.

        Returns:
            ListResponse: a ListResponse instance.
        """
        return self._list_resp(
            self.api.similarity_matrix.pages(
                offset, limit, name, type, description, version
            )
        )


    def add_similarity_matrix(
        self,
        name        : str,
        type        : SimilarityMatrixType,
        description : str,
        version     : int
    ):
        """

        Add a new similarity matrix. A similarity matrix is a dict dto with next structure:

        Examples:
            similarity_matrix = {
                'name'        : str,
                'type'        : api.SimilarityMatrixType [USER_TO_USER, ITEM_TO_ITEM],
                'description' : str,
                'version'     : int
            }

        Args:
            body (dict): Represent a similarity matrix dto.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix.add(body={
            'name'        : name,
            'type'        : type.value,
            'description' : description,
            'version'     : version
        }))


    def update_similarity_matrix(self, dto):
        """
        Update a similarity matrix with a given identifier. A similarity matrix is a dict dto with next structure:

        Examples:
            similarity_matrix = {
                'name'        : str,
                'type'        : int [USER_TO_USER = 1, ITEM_TO_ITEM = 2],
                'description' : str,
                'version'     : int
            }

        Args:
            body (dict): Represent a similarity matrix dto with updated values.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix.update(dto['id'], body = dto))


    def remove_similarity_matrix(self, id: int):
        """
        Remove a similarity matrix by a given identifier.

        Args:
            id (int): Similarity matrix identifier.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix.remove(id))


    def similarity_matrix_versions(self, id: int):
        """
        Query versions of a given similarity matrix. It method also allow as to query using pagination.

        Args:
            id (str): A similarity matrix identifier.

        Returns:
            ListResponse: a ListResponse instance.
        """
        return self._resp(self.api.similarity_matrix.versions(id))


    def remove_similarity_version(self, id: int, version: int):
        """
        Remove a similarity matrix version by a given identifier.

        Args:
            id (int): Similarity matrix version identifier.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix.remove_version(id, version))
    #--------------------------------------------------------------------------
    #
    #
    #
    #--------------------------------------------------------------------------
    # Similarity Matrix Cell
    #--------------------------------------------------------------------------
    def similarity_cells(
        self,
        offset : int = 0,
        limit  : int = 1,
        row    : str = '',
        column : str = '',
        matrix : str = ''
    ):
        """
        Query cells for a given similarity matrix. A similarity matrix cell is a dict dto with next structure:

        Examples:
            similarity_matrix_cell = {
                'row'     : int,
                'column'  : int,
                'value'   : float,
                'version' : int,
                'matrix'  : str, format: f'{host}/api/similarity-matrix/{SIMILARITY_MATRIX_ID}/'
            }

        It method also allow as to query using pagination an also filter by row, columns and matrix identifiers.

        Args:
            offset (int, optional): Page start from offset. Defaults to 0.
            limit (int, optional): Page size. Defaults to 10.
            row (str, optional): Similar matrix row identifier. Defaults to ''.
            column (str, optional): Similar matrix column identifier. Defaults to ''.
            matrix (str, optional): Similar matrix identifier. Defaults to ''.

        Returns:
            ListResponse: a ListResponse instance.
        """
        matrix = matrix.replace('$BASE_URL', self.host)
        return self._list_resp(
            self.api.similarity_matrix_cell.pages(
                offset, limit, row, column, matrix
            )
        )


    def bulk_add_similarity_cells(self, body):
        """

        Add new similarity cells in bulk way. A similarity matrix cell is a dict dto with next structure:

        Examples:
            similarity_matrix_cell = {
                'row'     : int,
                'column'  : int,
                'value'   : float,
                'version' : int,
                'matrix'  : str, format: f'{host}/api/similarity-matrix/{SIMILARITY_MATRIX_ID}/'
            }

        Args:
            body (an similarity matrix cel list): A list of dicts. Each dist represent an similarity matrix cell dto.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix_cell.add(body=body))


    def remove_similarity_cell(self, id: int):
        """
        Remove a similarity matrix cell by a given identifier.

        Args:
            id (int): Similarity matrix cell identifier.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.similarity_matrix_cell.remove(id))
    #--------------------------------------------------------------------------
    #
    #
    #
    #--------------------------------------------------------------------------
    # Recommender
    #--------------------------------------------------------------------------
    def recommenders(
        self,
        offset : int = 0,
        limit  : int = 1,
        name   : str = ''
    ):
        """
        Query recommenders. An recommender is a dict dto with next structure:

        Examples:
            recommender = {
                'id'                     : int,
                'name'                   : str,
                'user_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["user_similarity_matrix"]}/',
                'item_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["item_similarity_matrix"]}/'
            }

        Where user_similarity_matrix and item_similarity_matrix are identifier.
        It method also allow as to query using pagination an also filter by name.

        Args:
            offset (int, optional): Page start from offset. Defaults to 0.
            limit (int, optional): Page size. Defaults to 10.
            name (str, optional): Recommender name. Defaults to ''.

        Returns:
            ListResponse: a ListResponse instance.
        """
        return self._list_resp(self.api.recommenders.pages(offset, limit, name))


    def add_recommender(self, dto):
        """
        Add a new recommender. A recommender is a dict dto with next structure:

        Examples:
            recommender = {
                'id'                     : int,
                'name'                   : str,
                'user_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["user_similarity_matrix"]}/',
                'item_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["item_similarity_matrix"]}/'
            }

        Args:
            body (dict): Represent a recommender dto.
        Returns:
            ItemResponse: an ItemResponse object.
        """

        return self._resp(self.api.recommenders.add(body=dto))


    def update_recommender(self, dto):
        """
        update a recommender by a given identifier. A recommender is a dict dto with next structure:

        Examples:
            recommender = {
                'id'                     : int,
                'name'                   : str,
                'user_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["user_similarity_matrix"]}/',
                'item_similarity_matrix' : str - format: f'{host}/api/similarity-matrix/{model["item_similarity_matrix"]}/'
            }

        Args:
            body (dict): Represent a recommender dto with updated values.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.recommenders.update(dto['id'], body=dto))


    def remove_recommender(self, id: int):
        """
        Remove a recommender by a given identifier.

        Args:
            id (int): Recommender identifier.

        Returns:
            ItemResponse: an ItemResponse object.
        """
        return self._resp(self.api.recommenders.remove(id))
