import mysql.connector
from logger import get_logger


class Database:
    def __init__(self, config):
        self.connection = mysql.connector.connect(
          host     = config['host'],
          user     = config['user'],
          password = config['password']
        )
        self._logger = get_logger(self)

    def execute(self, query, buffered=True, select=False):
        try:
            cursor = self.connection.cursor(buffered=buffered)
            cursor.execute(query)
            if select:
                return cursor.fetchall()
            else:
                self.connection.commit()
            return None
        except Exception as error:
            self._logger.error(f'Error when execute query: {query}. {error}')
            return None


    def reset(self):
        self.execute('DELETE FROM recsys.recsysweb_interaction')
        self.execute('ALTER TABLE recsys.recsysweb_item MODIFY id int(11) NOT NULL')
        self.execute('ALTER TABLE recsys.recsysweb_item MODIFY id int(11) NOT NULL')
        self.execute('DELETE FROM recsys.recsysweb_item')
        self.execute('DELETE FROM recsys.taggit_taggeditem')
        self.execute('DELETE FROM recsys.taggit_tag')