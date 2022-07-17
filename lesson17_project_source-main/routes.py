from flask import current_app as app, request
from flask_restx import Api, Namespace, Resource
from models import db
from models import Movie, Director, Genre
import db_schema

api: Api = app.config['api']

movies_ns: Namespace = api.namespace('movies')
directors_ns: Namespace = api.namespace('directors')
genres_ns: Namespace = api.namespace('genres')

movie_schema = db_schema.Movie()
movies_schema = db_schema.Movie(many=True)

director_schema = db_schema.Director()
directors_schema = db_schema.Director(many=True)

genre_schema = db_schema.Genre()
genres_schema = db_schema.Genre(many=True)


@movies_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get(self, movie_id: int):
        # получение одного экземпляра фильма по movie_id из бд

        movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

        if movie is None:
            return None, 404

        return movie_schema.dump(movie), 200

    def put(self, movie_id: int):
        # обновляет кино по movie_id
        db.session.query(Movie).filter(Movie.id == movie_id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, movie_id: int):
        # удаляет фильм по movie_id
        db.session.query(Movie).filter(Movie.id == movie_id).delete()

        db.session.commit()
        return None, 200


@movies_ns.route('/')
class MoviesView(Resource):

    # получение всех экземпляров фильмов из бд
    def get(self):
        movies_all = db.session.query(Movie)

        args = request.args

        # возвращает фильмы по director_id
        director_id = args.get('director_id')
        if director_id is not None:
            movies_all = movies_all.filter(Movie.director_id == director_id)

        # возвращает фильмы по genre_id
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_all = movies_all.filter(Movie.genre_id == genre_id)

        movies = movies_all.all()

        return movies_schema.dump(movies), 200

    def post(self):

        # добавление нового фильма в базу данных
        movie = movie_schema.load(request.json)
        db.session.add(Movie(**movie))
        db.session.commit()

        return None, 201


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        # получение всех режиссеров
        directors_all = db.session.query(Director).all()

        return directors_schema.dump(directors_all), 200


@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):
    def get(self, director_id):
        # получение одного режиссера по director_id
        director = db.session.query(Director).filter(Director.id == director_id).one()

        if director is None:
            return None, 404

        return director_schema.dump(director), 200


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        # получение всех жанров

        genres = db.session.query(Genre).all()

        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def get(self, genre_id):
        # получение одного экземпляра по genre_id

        genre = db.session.query(Genre).filter(Genre.id == genre_id).one()

        if genre is None:
            return None, 404

        return genre_schema.dump(genre), 200
