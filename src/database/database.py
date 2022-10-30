import mysql.connector
import logging


class Database:
    def __init__(self, config):
        self.connection = mysql.connector.connect(
          host     = config['host'],
          user     = config['user'],
          password = config['password']
        )

    def execute(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Exception as error:
            logging.error(f'Error when execute query: {query}. {error}')
