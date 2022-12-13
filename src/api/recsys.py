from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from sklearn.utils import Bunch
from enum import Enum
import bunch
import json
import logging
import pandas as pd


class ListResponse:
    def __init__(self, status, body):
        self.status = status
        self.body   = bunch.Bunch(body)
        if 'results' in body:
            self.body.results = [bunch.Bunch(item) for item in self.body.results]

    def __repr__(self): return self.__str__()
    def __str__(self):  return json.dumps({'status': self.status, 'body': self.body}, indent=4)


class ItemResponse:
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
    def create(name, filters=''):
        return {
            'pages':  { 'method': 'GET',    'url': "/api/"+ name + "/?offset={}&limit={}" + filters },
            'add':    { 'method': 'POST',   'url': "/api/"+ name + "/" },
            'update': { 'method': 'PUT',    'url': "/api/"+ name + "/{}/" },
            'remove': { 'method': 'DELETE', 'url': "/api/"+ name + "/{}/" }
        }


class SimilarityMatrixType(Enum):
    USER_TO_USER = 1
    ITEM_TO_ITEM = 2


class UserResource(Resource):
    actions = ActionsFactory.create('users', '&username={}&email={}')

class ItemResource(Resource):
    actions = ActionsFactory.create('items', '&name={}&description={}' )

class InteractionResource(Resource):
    actions = ActionsFactory.create('interactions', '&user={}&item={}')

class SimilarityMatrixResource(Resource):
    actions = ActionsFactory.create(
        'similarity-matrix',
        'name={}&type={}&description={}&version={}'
    )


class SimilarityMatrixCellResource(Resource):
    actions = ActionsFactory.create(
        'similarity-matrix-cells',
        '&row={}&column={}&matrix={}'
    )

class RecommenderResource(Resource):
    actions = ActionsFactory.create('recommenders', '&name={}')


"""
https://python-simple-rest-client.readthedocs.io/en/latest/quickstart.html
"""
class RecSysApi:
    def __init__(self, token, host='http://localhost:8000', timeout=500):
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
            resource_name  = 'interations',
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
    def items(self, offset=0, limit=10, name='', description=''):
        return self._list_resp(self.api.items.pages(
            offset, limit, name, description
        ))


    # Interactions
    def interactions(self, offset=0, limit=10, user='', item=''):
        return self._list_resp(self.api.interations.pages(
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
        return self._resp(self.api.similarity_matrix.add(body={
            'name'        : name,
            'type'        : type.value,
            'description' : description,
            'version'     : version
        }))

    def update_similarity_matrix(self, dto):
        return self._resp(self.api.similarity_matrix.update(dto['id'], body = dto))

    def remove_similarity_matrix(self, id: int):
        return self._resp(self.api.similarity_matrix.remove(id))
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
        matrix = matrix.replace('$BASE_URL', self.host)
        return self._list_resp(
            self.api.similarity_matrix_cell.pages(
                offset, limit, row, column, matrix
            )
        )

    def bulk_add_similarity_cells(self, body):
        return self._resp(self.api.similarity_matrix_cell.add(body=body))

    def remove_similarity_cell(self, id: int):
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
        return self._list_resp(self.api.recommenders.pages(offset, limit, name))

    def add_recommender(self, dto):
        return self._resp(self.api.recommenders.add(body=dto))

    def update_recommender(self, dto):
        return self._resp(self.api.recommenders.update(dto['id'], body=dto))

    def remove_recommender(self, id: int):
        return self._resp(self.api.recommenders.remove(id))
