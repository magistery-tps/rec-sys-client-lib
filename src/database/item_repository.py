from .repository import Repository


class ItemRepository(Repository):
    def __init__(self, database): super().__init__(database)
    def save(self, row):
        query = """
            INSERT INTO
                recsys.recsysweb_item(id, name, description, image, popularity)
            VALUES (
                :ID,
                ":NAME",
                ":DESC",
                ":IMAGE",
                0
            );
            """.replace(':ID', str(row['id'])) \
                .replace(':NAME', str(row['name'])) \
                .replace(':DESC', str(row['description']).replace('"', '')) \
                .replace(':IMAGE', str(row['image']))
        self.database.execute(query)


    def find_all(self):
        return self.database.execute("SELECT id, name, description, image, popularity FROM recsys.recsysweb_item")
