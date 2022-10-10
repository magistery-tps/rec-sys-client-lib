import requests
import logging


class TMDbApi:
    def poster_url_by_id(self, movie_id):
        try:
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        except:
            logging.error(f'Error to build poster url for {str(movie_id)} movie_id!')
            return None