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
    actions = ActionsFactory.create('similarity-matrix', '&name={}&type={}&description={}')


class SimilarityMatrixCellResource(Resource):
    actions = ActionsFactory.create('similarity-matrix-cells', '&row={}&column={}&matrix={}')


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
        api.add_resource(resource_name='users', resource_class=UserResource)
        api.add_resource(resource_name='items', resource_class=ItemResource)
        api.add_resource(resource_name='interations', resource_class=InteractionResource)
        api.add_resource(resource_name='similarity_matrix', resource_class=SimilarityMatrixResource)
        api.add_resource(resource_name='similarity_matrix_cell', resource_class=SimilarityMatrixCellResource)
        self.api = api

    def _resp(self, response): return ItemResponse(response.status_code, response.body)

    def _list_resp(self, response): return ListResponse(response.status_code, response.body)


    # Users
    def users(self, offset=0, limit=10, username='', email=''):
        return self._list_resp(self.api.users.pages(offset, limit, username, email))


    # Items
    def items(self, offset=0, limit=10, name='', description=''):
        return self._list_resp(self.api.items.pages(offset, limit, name, description))


    # Interactions
    def interactions(self, offset=0, limit=10, user='', item=''):
        return self._list_resp(self.api.interations.pages(offset, limit, user, item))


    # Similarity Matrix
    def similarity_matrix(self, offset=0, limit=10, name='', type='', description=''):
        return self._list_resp(self.api.similarity_matrix.pages(offset, limit, name, type, description))


    def add_similarity_matrix(self, name, type: SimilarityMatrixType, description):
        return self._resp(self.api.similarity_matrix.add(body={
            'name': name,
            'type': type.value,
            'description': description
        }))


    def remove_similarity_matrix(self, id): return self._resp(self.api.similarity_matrix.remove(id))


    def add_or_get_similarity_matrix(self, name, type, description):
        response = self.similarity_matrix(name=name)
        if len(response.body.results) > 0 and response.body.results[0].name == name:
            logging.info(f'{name} of type {type} already exists!')
            return response.body.results[0]
        else:
            logging.info(f'Insert {name} of type {type}.')
            response = self.add_similarity_matrix(name, type, description)
            return response.body


    # Similarity Matrix Cells
    def similarity_cells(self, offset=0, limit=1, row='', column='', matrix=''):
        return self._list_resp(self.api.similarity_matrix_cell.pages(offset, limit, row, column, matrix))


    def add_similarity_cell(self, row, column, value, matrix):
        return self._resp(self.api.similarity_matrix_cell.add(body={
            'row'   : row,
            'column': column,
            'value' : value,
            'matrix': f'http://localhost:8000/api/similarity-matrix/{matrix}/'
        }))

    def add_similarity_cells(self, cells: pd.DataFrame):
        body = []
        for _, row in cells.iterrows():
            body.append({
                'row'   : row['row'],
                'column': row['column'],
                'value' : row['value'],
                'matrix': f'http://localhost:8000/api/similarity-matrix/{row["matrix"]}/'
            })
        return self._resp(self.api.similarity_matrix_cell.add(body=body))

    def remove_similarity_cell(self, id): return self._resp(self.api.similarity_matrix_cell.remove(id))
