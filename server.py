from director.directors_pb2_grpc import  add_DirectorsServiceServicer_to_server
from genre.genres_pb2_grpc import add_GenresServiceServicer_to_server
from movie.movies_pb2_grpc import add_MoviesServiceServicer_to_server
from flask import Flask, jsonify, make_response
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from database.database import Database
from spyne import Application
from concurrent import futures
from soap import *
from grpc_ import *
import grpc
import asyncio

#Flask
app = Flask(__name__)

#------------------------------------------------------------------------------------------------------------------------
#SOAP
#------------------------------------------------------------------------------------------------------------------------

#Konfiguracja serwera i opcji protokołu
application_movies = Application([MoviesService], 'movies', in_protocol=Soap11(), out_protocol=Soap11())
application_directors = Application([DirectorsService], 'directors', in_protocol=Soap11(), out_protocol=Soap11())
application_genres = Application([GenresService], 'genres', in_protocol=Soap11(), out_protocol=Soap11())

#Adapter dopasowania do serwerów WWW
wsgi_application_movies = WsgiApplication(application_movies)
wsgi_application_directors = WsgiApplication(application_directors)
wsgi_application_genres = WsgiApplication(application_genres)

#------------------------------------------------------------------------------------------------------------------------
#REST
#------------------------------------------------------------------------------------------------------------------------

#FILMY
@app.route('/rest/movies', methods=['GET'])
def get_movies():
    #Pobierz informacje z bazy danych
    database = Database()
    movies = database.get_table('movies')
    database.close_connection()
    movies_list = []

    #Sformatuj dane
    for movie in movies:
        key = ["id", "title", "description", "director_id", "genre_id"]
        values = movie
        movie_dictionary = dict(zip(key, values))
        movies_list.append(movie_dictionary)

    #Zwróć odpowiedź w postaci JSON
    return jsonify({'movies': movies_list})

@app.route('/rest/movie/<int:id>', methods=['GET'])
def get_movie(id):
    database = Database()
    movie = database.get_table('movies',str(id))
    database.close_connection()

    #Sformatuj dane
    key = ["id", "title", "description", "director_id", "genre_id"]
    try:
        values = movie[0]
    except:
        #Gdy nie ma w bazie danych zwróć błąd w postaci JSON
        error = jsonify({"error" : 404, "description" : "Movie not found"})
        return make_response(error, 404)

    movie_dictionary = dict(zip(key, values))

    #Zwróć odpowiedź w postaci JSON
    return jsonify({'movie': movie_dictionary})

#------------------------------------------------------------------------------------------------------------------------

#REŻYSERZY
@app.route('/rest/directors', methods=['GET'])
def get_directors():
    #Pobierz informacje z bazy danych
    database = Database()
    directors = database.get_table('directors')
    database.close_connection()
    directors_list = []

    #Sformatuj dane
    for director in directors:
        key = ["id", "name", "surname"]
        values = director
        director_dictionary = dict(zip(key, values))
        directors_list.append(director_dictionary)

    #Zwróć odpowiedź w postaci JSON
    return jsonify({'directors': directors_list})
    
@app.route('/rest/director/<int:id>', methods=['GET'])
def get_director(id):
    database = Database()
    director = database.get_table('directors',str(id))
    database.close_connection()

    #Sformatuj dane
    key = ["id", "name", "surname"]
    try:
        values = director[0]
    except:
        #Gdy nie ma w bazie danych zwróć błąd w postaci JSON
        error = jsonify({"error" : 404, "description" : "Director not found"})
        return make_response(error, 404)

    director_dictionary = dict(zip(key, values))

    #Zwróć odpowiedź w postaci JSON
    return jsonify({'director': director_dictionary})

#------------------------------------------------------------------------------------------------------------------------

#GATUNKI
@app.route('/rest/genres', methods=['GET'])
def get_genres():
        #Pobierz informacje z bazy danych
        database = Database()
        genres = database.get_table('genres')
        database.close_connection()
        genres_list = []

        #Sformatuj dane
        for genre in genres:
            key = ["id", "name"]
            values = genre
            genre_dictionary = dict(zip(key, values))
            genres_list.append(genre_dictionary)

        #Zwróć odpowiedź w postaci JSON
        return jsonify({'genres': genres_list})

@app.route('/rest/genre/<int:id>', methods=['GET'])
def get_genre(id):
    database = Database()
    genre = database.get_table('genres',str(id))
    database.close_connection()

    #Sformatuj dane
    key = ["id", "name"]
    try:
        values = genre[0]
    except:
        #Gdy nie ma w bazie danych zwróć błąd w postaci JSON
        error = jsonify({"error" : 404, "description" : "Genre not found"})
        return make_response(error, 404)

    genre_dictionary = dict(zip(key, values))

    #Zwróć odpowiedź w postaci JSON
    return jsonify({'genre': genre_dictionary})

#------------------------------------------------------------------------------------------------------------------------
#SOAP
#------------------------------------------------------------------------------------------------------------------------

#Podpięcie ścieżek
@app.route("/soap/movies", methods=['POST'])
def movies():
    return wsgi_application_movies

@app.route("/soap/directors", methods=['POST'])
def directors():
    return wsgi_application_directors

@app.route("/soap/genres", methods=['POST'])
def genres():
    return wsgi_application_genres

#------------------------------------------------------------------------------------------------------------------------
#gRPC
#------------------------------------------------------------------------------------------------------------------------

#Utwórz nowy obiekt serwera
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

#Implementacja metod
add_MoviesServiceServicer_to_server(Movies(), server)
add_DirectorsServiceServicer_to_server(Directors(), server)
add_GenresServiceServicer_to_server(Genres(), server)

#------------------------------------------------------------------------------------------------------------------------

#Asynchroniczne uruchomienie
async def server_flask():
    #Uruchomienie serwera
    print('Uruchamianie serwera Flask')
    app.run(debug=True)

async def server_grpc():
    #Uruchomienie serwera
    print('Uruchamianie serwera gRPC')
    server.add_insecure_port('[::]:50051')
    server.start()
    
async def main():
    await asyncio.gather(server_grpc(),server_flask())

if __name__ == "__main__":
    #Główna część programu
    asyncio.run(main())