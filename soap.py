from spyne import rpc, ServiceBase, Iterable
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, String, Unicode
from database.database import Database

#------------------------------------------------------------------------------------------------------------------------

#Format zwracanych danych
class Movie(ComplexModel):
    id = Integer
    title = String
    description = String
    director_id = Integer
    genre_id = Integer

class Director(ComplexModel):
    id = Integer
    name = String
    surname = String

class Genre(ComplexModel):
    id = Integer
    name = String

#W przypdaku zapyania o konkretny film - przygotuj ewentualność błędu
class MovieResponse(ComplexModel):
    movie = Movie.customize(min_occurs=0)
    error = Unicode(min_occurs=0)

class DirectorResponse(ComplexModel):
    director = Director.customize(min_occurs=0)
    error = Unicode(min_occurs=0)

class GenreResponse(ComplexModel):
    genre = Genre.customize(min_occurs=0)
    error = Unicode(min_occurs=0)

#------------------------------------------------------------------------------------------------------------------------

#Mechanizmy do obsługi żądań i odpowiedzi SOAP
class MoviesService(ServiceBase):
    @rpc(_returns=Iterable(Movie))
    def get_movies(self):

        #Pobierz informacje z bazy danych
        database = Database()
        movies = database.get_table('movies')
        database.close_connection()

        #Zrwóć odpowiedź w postaci XML
        for movie in movies:
            yield Movie(id=movie[0], title=movie[1], description=movie[2], director_id=movie[3], genre_id=movie[4])
    
    @rpc(Integer, _returns=MovieResponse)
    def get_movie(self, id: int):

        #Pobierz informacje z bazy danych
        database = Database()
        movie = database.get_table('movies',str(id))
        database.close_connection()

        #Przygotuj odpowiedź
        response = MovieResponse()

        #Jeśli film o id istnieje zrwóć odpowiedź w postaci XML
        try:
            if movie[0][0] == id:
                response.movie = movie[0]
                return response
                
        #W przeciwnym wypadku zwróć błąd w postaci XML
        except:
            response.error = f'No found'
            return response

class DirectorsService(ServiceBase):
    @rpc(_returns=Iterable(Director))
    def get_directors(self):

        #Pobierz informacje z bazy danych
        database = Database()
        directors = database.get_table('directors')
        database.close_connection()

        #Zrwóć odpowiedź w postaci XML
        for director in directors:
            yield Director(id=director[0], name=director[1], surname=director[2])
    
    @rpc(Integer, _returns=DirectorResponse)
    def get_director(self, id: int):

        #Pobierz informacje z bazy danych
        database = Database()
        director = database.get_table('directors',str(id))
        database.close_connection()

        #Przygotuj odpowiedź
        response = DirectorResponse()

        #Jeśli film o id istnieje zrwóć odpowiedź w postaci XML
        try:
            if director[0][0] == id:
                response.director = director[0]
                return response
                
        #W przeciwnym wypadku zwróć błąd w postaci XML
        except:
            response.error = f'No found'
            return response

class GenresService(ServiceBase):
    @rpc(_returns=Iterable(Genre))
    def get_genres(self):

        #Pobierz informacje z bazy danych
        database = Database()
        genres = database.get_table('genres')
        database.close_connection()

        #Zrwóć odpowiedź w postaci XML
        for genre in genres:
            yield Genre(id=genre[0], name=genre[1])
    
    @rpc(Integer, _returns=GenreResponse)
    def get_genre(self, id: int):

        #Pobierz informacje z bazy danych
        database = Database()
        genre = database.get_table('genres',str(id))
        database.close_connection()

        #Przygotuj odpowiedź
        response = GenreResponse()

        #Jeśli film o id istnieje zrwóć odpowiedź w postaci XML
        try:
            if genre[0][0] == id:
                response.genre = genre[0]
                return response
                
        #W przeciwnym wypadku zwróć błąd w postaci XML
        except:
            response.error = f'No found'
            return response

#------------------------------------------------------------------------------------------------------------------------