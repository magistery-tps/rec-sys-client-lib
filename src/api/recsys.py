from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from sklearn.utils import Bunch


class ActionsFactory:
    @staticmethod
    def create(name):
        return {
            'pages':  { 'method': 'GET',    'url': "/api/"+ name + "/?offset={}&limit={}" },
            'add':    { 'method': 'POST',   'url': "/api/"+ name + "/"    },
            'update': { 'method': 'PUT',    'url': "/api/"+ name + "/{}/" },
            'remove': { 'method': 'DELETE', 'url': "/api/"+ name + "/{}/" }
        }

class UserResource(Resource):
    actions = ActionsFactory.create('users')

class ItemResource(Resource):
    actions = ActionsFactory.create('items')

class InteractionResource(Resource):
    actions = ActionsFactory.create('interactions')

class DistanceMatrixResource(Resource):
    actions = ActionsFactory.create('distances-matrix')

class DistanceMatrixCellResource(Resource):
    actions = ActionsFactory.create('distances-matrix-cells')


class RecSysApi:
    def __init__(self, token, host='http://localhost:8000'):
        headers = {'Authorization': f'Token {token}'}
        api = API(
            api_root_url     = host,
            headers          = headers,
            json_encode_body = True
        )
        api.add_resource(resource_name='users', resource_class=UserResource)
        api.add_resource(resource_name='items', resource_class=ItemResource)
        api.add_resource(resource_name='interations', resource_class=InteractionResource)
        api.add_resource(resource_name='distances_matrix', resource_class=DistanceMatrixResource)
        api.add_resource(resource_name='distances_matrix_cell', resource_class=DistanceMatrixCellResource)
        self.api = api

    def _resp(self, response): return Bunch(status=response.status_code, body=response.body)


    def users(self, offset=0, limit=1): return self._resp(self.api.users.pages(offset, limit))

    def items(self, offset=0, limit=1): return self._resp(self.api.items.pages(offset, limit))
    
    def interactions(self, offset=0, limit=1): return self._resp(self.api.interations.pages(offset, limit))

    # Distances

    def distances_matrix(self, offset=0, limit=1): return self._resp(self.api.distances_matrix.pages(offset, limit))

    def add_distances_matrix(self, name, description):
        return self._resp(self.api.distances_matrix.add(body={
            'name': name, 
            'description': description
        }))

    def remove_distances_matrix(self, id): return self._resp(self.api.distances_matrix.remove(id))

    # Cells

    def distance_cells(self, offset=0, limit=1): return self._resp(self.api.distances_matrix_cell.pages(offset, limit))

    def add_distance_cell(self, row, column, value, matrix):
        return self._resp(self.api.distances_matrix_cell.add(body={
            'row'   : row,
            'column': column,
            'value' : value,
            'matrix': f'http://localhost:8000/api/distances-matrix/{matrix}/'
        }))

    def remove_distance_cell(self, id): return self._resp(self.api.distances_matrix_cell.remove(id))
