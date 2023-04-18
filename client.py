from director.directors_pb2_grpc import DirectorsServiceStub
from movie.movies_pb2_grpc import MoviesServiceStub
from genre.genres_pb2_grpc import GenresServiceStub
from google.protobuf.empty_pb2 import Empty
import matplotlib.pyplot as plt
from xml.dom import minidom
import numpy as np
import requests
import time
import json
import grpc


class Client:

    #Konfiguracja - Inicjalizacja
    def __init__(self, print_response_body=False, print_response_time=True, element_response="movies"):
        self.print_response_body=print_response_body
        self.print_response_time=print_response_time
        self.element_response=element_response

    def rest(self):
        print('---REST---')

        #Zapytanie do REST API
        start_time = time.time()
        response = requests.get('http://127.0.0.1:5000/rest/{}'.format(self.element_response))
        end_time = time.time()

        #Zapisz zmienną w obiekcie
        self.rest_time = end_time - start_time

        #Pokazanie otrzymanych danych
        if self.print_response_time == True:
            print('Response time: {}'.format(self.rest_time))

        if self.print_response_body == True:
            print(json.dumps(response.json(), indent=4))


    def soap(self):
        print('---SOAP---')

        #Przygotowanie XML zmiennej
        data = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:{}="{}">
            <soapenv:Header/>
                <soapenv:Body>
                    <{}:get_{}/>
                </soapenv:Body>
        </soapenv:Envelope>
        '''.format(self.element_response,self.element_response,self.element_response,self.element_response)

        #Zapytanie do SOAP API
        start_time = time.time()
        response = requests.post('http://127.0.0.1:5000/soap/{}'.format(self.element_response), headers={'content-type': 'application/soap+xml'}, data=data)
        end_time = time.time()

        #Zapisz zmienną w obiekcie
        self.soap_time = end_time - start_time

        #Pokazanie otrzymanych danych
        if self.print_response_time == True:
            print('Response time: {}'.format(self.soap_time))

        if self.print_response_body == True:
            xmldoc = minidom.parseString(response.content)
            print(xmldoc.toprettyxml(indent="    ", newl='\n', encoding='UTF-8').decode())


    def grpc(self):
        print('---gRPC---')

        #Przygotowanie kanału
        channel = grpc.insecure_channel('localhost:50051')

        #Przygotowanie map
        class_map = {
            'movies': MoviesServiceStub,
            'directors': DirectorsServiceStub,
            'genres': GenresServiceStub
        }

        #Przygotowanie zmiennych
        stub = class_map[self.element_response](channel)
        method_name = 'get_{}'.format(self.element_response)

        #Zapytanie do gRPC API
        start_time = time.time()
        response = getattr(stub, method_name)(Empty())
        end_time = time.time()

        #Zapisz zmienną w obiekcie
        self.grpc_time = end_time - start_time

        #Pokazanie otrzymanych danych
        if self.print_response_time == True:
            print('Response time: {}'.format(self.grpc_time))

        if self.print_response_body == True:
            if self.element_response == 'movies':
                for movie in response:
                    print(movie.id, movie.title, movie.description, movie.director_id, movie.genre_id)
            elif self.element_response == 'directors':
                for director in response:
                    print(director.id, director.name, director.surname)
            elif self.element_response == 'genres':
                for genre in response:
                    print(genre.id, genre.name)

    def matplotlib(self):
        try:
            #Przygotuj dane
            height = [self.rest_time, self.soap_time, self.grpc_time]
            bars = ('REST', 'SOAP', 'gRPC')
            y_pos = np.arange(len(height))
            
            #Ustaw rozmiar okna
            plt.figure(figsize=(10,5))
            
            #Ustaw bars
            plt.bar(y_pos, height, color = 'blue')
            
            #Ustaw nazwy dla interfe
            plt.xticks(y_pos, bars)
            
            #Ustaw label'e
            plt.xlabel('Interfejs', fontsize=12, color='#323232')
            plt.ylabel('Czas odpowiedzi', fontsize=12, color='#323232')
            plt.title('Interfejsy komunikacyjne REST SOAP gRPC', fontsize=16, color='#323232')
            
            #Pokaż wykres
            plt.show()
        except:
            print('No data')


if __name__ == "__main__":
    client = Client()
    client.rest()
    client.soap()
    client.grpc()
    client.matplotlib()