import grpc
from director.directors_pb2 import Director
from director.directors_pb2_grpc import DirectorsServiceServicer
from genre.genres_pb2 import Genre
from genre.genres_pb2_grpc import GenresServiceServicer
from movie.movies_pb2 import Movie
from movie.movies_pb2_grpc import MoviesServiceServicer
from database.database import Database

#------------------------------------------------------------------------------------------------------------------------

#FILMY
class Movies(MoviesServiceServicer):
    def get_movies(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        movies = database.get_table('movies')
        database.close_connection()

        #Zwróć dane
        for movie in movies:
            yield Movie(id=movie[0], title=movie[1], description=movie[2], director_id=movie[3], genre_id=movie[4])

    def get_movie(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        movie = database.get_table('movies',str(request.id))
        database.close_connection()

        #Sformatuj dane
        try:
            movie = movie[0]
        except:
            #Gdy nie ma w bazie danych zwróć błąd
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Movie not found")
            return None
        
        #Gdy wszystko ok zwróć dane
        return Movie(id=movie[0], title=movie[1], description=movie[2], director_id=movie[3], genre_id=movie[4])

#REŻYSERZY
class Directors(DirectorsServiceServicer):
    def get_directors(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        directors = database.get_table('directors')
        database.close_connection()

        #Zwróć dane
        for director in directors:
            yield Director(id=director[0], name=director[1], surname=director[2])

    def get_director(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        director = database.get_table('directors',str(request.id))
        database.close_connection()

        #Sformatuj dane
        try:
            director = director[0]
        except:
            #Gdy nie ma w bazie danych zwróć błąd
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Director not found")
            return None

        #Gdy wszystko ok zwróć dane
        return Director(id=director[0], name=director[1], surname=director[2])

#GATUNKI
class Genres(GenresServiceServicer):
    def get_genres(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        genres = database.get_table('genres')
        database.close_connection()

        for genre in genres:
            yield Genre(id=genre[0], name=genre[1])

    def get_genre(self, request, context):
        #Pobierz informacje z bazy danych
        database = Database()
        genre = database.get_table('genres',str(request.id))
        database.close_connection()

        #Sformatuj dane
        try:
            genre = genre[0]
        except:
            #Gdy nie ma w bazie danych zwróć błąd
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Genre not found")
            return None
        
        #Gdy wszystko ok zwróć dane
        return Genre(id=genre[0], name=genre[1])

#------------------------------------------------------------------------------------------------------------------------
