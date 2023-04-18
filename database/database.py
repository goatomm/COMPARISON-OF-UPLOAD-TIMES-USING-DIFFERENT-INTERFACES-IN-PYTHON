import mysql.connector

class Database:
    def __init__(self, user='root', password='', host='localhost', database='python'):
        try:
            #Połączenie z bazą danych MySQL z XAMPP
            self.cnx = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=database
            )
            #Utwórz kursor - operacje na bazie danych
            self.cursor = self.cnx.cursor()
            print('Utworzono połączenie z bazą danych')
        except:
            print('Nie udało się nawiązać połączenia z bazą danych')
    
    def create_tables(self):
        try:
            #Utworz tabele
            self.cursor.execute("CREATE TABLE movies (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255))")
            self.cursor.execute("CREATE TABLE directors (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255))")
            self.cursor.execute("CREATE TABLE genres (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

            #Utworz relacje
            self.cursor.execute("ALTER TABLE movies ADD director_id INT, ADD FOREIGN KEY (director_id) REFERENCES directors(id)")
            self.cursor.execute("ALTER TABLE movies ADD genre_id INT, ADD FOREIGN KEY (genre_id) REFERENCES genres(id)")

            #Zapisz w bazie
            self.cnx.commit()
            print('Utworzono tabelę')
        except:
            print('Nie można było utworzyć tabeli')

    def add_movie(self, title, description, directorName, directorSurname, genre):
        #Sprawdzanie czy tytuł już istnieje
        self.cursor.execute("SELECT * FROM movies WHERE title = %s", (title,))
        if self.cursor.fetchone():
            print("Film o takim tytule już istnieje.")
            return

        #Sprawdzanie czy reżyser już istnieje
        self.cursor.execute("SELECT id FROM directors WHERE name = %s AND surname = %s", (directorName,directorSurname))
        director_id = self.cursor.fetchone()

        #Przygotowanie zmiennej
        try:
            director_id = director_id[0]
        except:
            pass

        if not director_id:
            #Dodawanie reżysera do tabeli
            self.cursor.execute("INSERT INTO directors (name, surname) VALUES (%s, %s)", (directorName,directorSurname))
            director_id = self.cursor.lastrowid
            print('Dodanie nowego reżysera do tabeli')
        else:
            print('Skorzystanie z istniejącego reżysera w tabeli')

        #Sprawdzanie czy gatunek już istnieje
        self.cursor.execute("SELECT id FROM genres WHERE name = %s", (genre,))
        genre_id = self.cursor.fetchone()

        #Przygotowanie zmiennej
        try:
            genre_id = genre_id[0]
        except:
            pass

        if not genre_id:
            #Dodawanie gatunku do tabeli
            self.cursor.execute("INSERT INTO genres (name) VALUES (%s)", (genre,))
            genre_id = self.cursor.lastrowid
            print('Dodanie nowego gatunku do tabeli')
        else:
            print('Skorzystanie z istniejącego gatunku w tabeli')

        #Dodawanie filmu do tabeli z odpowiednim reżyserem i gatunkiem
        self.cursor.execute("INSERT INTO movies (title, description, director_id, genre_id) VALUES (%s, %s, %s, %s)", (title, description, director_id, genre_id))
        self.cnx.commit()
        print('Film dodany z powodzeniem')

    def get_table(self, table, id=''):
        if id != '':
            id = 'WHERE id = '+id
        self.cursor.execute("SELECT * FROM {} {}".format(table, id))
        return self.cursor.fetchall()

    
    def close_connection(self):
        self.cnx.close()
        print('Zakończono połączenie z bazą danych')