import requests
from logger import get_logger


class TMDbData:
    def __init__(self, data):
        self.data = data
        self.logger = get_logger(self)

    @property
    def poster(self): return "https://image.tmdb.org/t/p/w500/" + self.data['poster_path']

    @property
    def imdb_id(self): return self.data['imdb_id']

    @property
    def genres(self): return [genre['name'] for genre in self['genres']]

    @property
    def language(self): return self.data['original_language']

    @property
    def overview(self): return self.data['overview']

    @property
    def release_date(self): return self.data['release_date']

    @property
    def popularity(self): return self.data['popularity']

    @property
    def vote_average(self): return self.data['vote_average']

    @property
    def vote_count(self): return self.data['vote_count']

    @property
    def adult(self): return self.data['adult']

    @property
    def budget(self): return self.data['budget']

    @property
    def title(self): return self.data['original_title']


class TMDbApi:
    def movie_by(self, movie_id):
        try:
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
            data = requests.get(url)
            return TMDbData(data.json())
        except:
            self.logger.error(f'Error to build poster url for {str(movie_id)} movie_id!')
            return None
