from .repository import Repository


class ItemRepository(Repository):
    def __init__(self, database): super().__init__(database)
    def save(self, row):
        query = """
            INSERT INTO 
                recsys.recsysweb_item(id, name, description, image)
            VALUES (
                :ID,
                ":NAME",
                ":DESC",
                ":IMAGE"
            );    
            """.replace(':ID', str(row['id'])) \
                .replace(':NAME', str(row['name'])) \
                .replace(':DESC', str(row['description']).replace('"', '')) \
                .replace(':IMAGE', str(row['image']))
        self.database.execute(query)