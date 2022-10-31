from .repository import Repository


class InteractionRepository(Repository):
    def __init__(self, database): super().__init__(database)
    def save(self, row):
        query = """
            INSERT INTO 
                recsys.recsysweb_interaction(item_id, user_id, rating)
            VALUES (
                ":ITEM_ID",
                ":USER_ID",
                ":RATING"
            );    
            """.replace(':ITEM_ID', str(int(row['item_id']))) \
                .replace(':USER_ID', str(int(row['user_id']))) \
                .replace(':RATING', str(row['rating']))
        self.database.execute(query)