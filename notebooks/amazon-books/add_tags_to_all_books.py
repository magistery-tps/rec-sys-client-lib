from recsysweb.models import Item
import pickle

def load(path):
    with open(f'{path}.pickle', 'rb') as handle:
        return pickle.load(handle)
    
books = load('./books_genres')
filtered_books = [(name, genres) for (name, genres) in books.items() if len(genres) > 0]




for (name, genres) in filtered_books:
    result = Item.objects.filter(name=name)
    if len(result) > 0:
        item = result[0]
        for g in genres:
            item.tags.add(g)