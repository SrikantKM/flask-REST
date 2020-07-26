from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Movies Class/Model


class Movie(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    popularity = db.Column(db.Integer)
    director = db.Column(db.String(100), unique=True)
    genre = db.Column(db.String(200))
    imdb_score = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, popularity, director, genre, imdb_score, name):
        self.popularity = popularity
        self.director = director
        self.genre = genre
        self.imdb_score = imdb_score
        self.name = name

# Movies schema


class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('popularity', 'director', 'genre', 'imdb_score', 'name')


# Init schema
movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)

# Add a movie
@app.route('/movie', methods=['POST'])
def add_movie():
    popularity = request.json['popularity']
    director = request.json['director']
    genre = request.json['genre']
    imdb_score = request.json['imdb_score']
    name = request.json['name']

    new_movie = Movie(popularity,director,genre,imdb_score,name)

    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)

# Get all the movies
@app.route('/movies', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result.data)

# Get single movie
@app.route('/movie/<id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    return movie_schema.jsonify(movie)

# Update a movie
@app.route('/movie/<id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)

    popularity = request.json['popularity']
    director = request.json['director']
    genre = request.json['genre']
    imdb_score = request.json['imdb_score']
    name = request.json['name']

    movie.popularity = popularity
    movie.director = director
    movie.genre = genre
    movie.imdb_score = imdb_score
    movie.name = name

    db.session.commit()

    return movie_schema.jsonify(movie)

# Delete single movie
@app.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return movie_schema.jsonify(movie)


# Run server
if __name__ == "__main__":
    app.run(debug=True)

