import numpy as np
import api
from repository import InteractionRepository


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository


    def find_all(self, page_size):
        return self.repository.find_all(page_size)

    
    def rated_items_by_user(self, df, min_rating=0):
        result = {}
        for _, row in df.iterrows():
            if row['rating'] != None and row['rating'] > min_rating:
                if row['user_id'] in result:
                    result[row['user_id']].add(row['item_id'])
                else:
                    result[row['user_id']] = set([row['item_id']])
        return result


    def unrated_items_by_users(self, df, min_rating=0):
        all_items           = set(np.unique(df['item_id'].values))
        rated_items_by_user = self.rated_items_by_user(df, min_rating)
        result              = {user: list(all_items-user_rated_items) for user, user_rated_items in rated_items_by_user.items()}

        del rated_items_by_user
        del all_items

        return result