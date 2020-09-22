from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import requests
from bs4 import BeautifulSoup
import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

   # Create event

    url = 'https://www.cineslarambla.es/filmoteca/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    code_dates = soup.find_all('div', {'class': 'n module-type-text diyfeLiveArea'})

    movie_dates = []
    for i in range(2,len(code_dates)):
        movie_dates.append(code_dates[i].text.strip().replace("\xa0",''))


    titles = soup.find_all('div', {'class': 'n module-type-textWithImage diyfeLiveArea'})


    lines = []
    for i in range(len(titles)):
        text = titles[i].find_all('p')
        for line in text:
            if line.text == '\xa0' or line.text == 'Sinopsis:':
                continue
            lines.append(line.text.replace('\n',' '))

    pp = pprint.PrettyPrinter(indent=4)

    # Stores list in triples 
    movie_texts = [lines[i:i + 3] for i in range(0, len(lines), 3)]
    
    keys = ['movie_title', 'genre', 'synopsis']
    
    # Generate a list of dicts
    dict_movies = [dict(zip(keys, l)) for l in movie_texts]

    # print(movie_dates)
    # pp.pprint(dict_movies)
    
    for i in range(len(movie_dates)):
        event = {
          'summary': '🎬 ' + dict_movies[i]['movie_title'],
          'location': 'Cines La Rambla, Av. de los Príncipes de España, 0, 28821 Coslada, Madrid',
          'description': dict_movies[i]['genre'] + '\n' + dict_movies[i]['synopsis'] + '\nhttps://www.cineslarambla.es/filmoteca/',
          'start': {
            'date': str_to_date(movie_dates[i])
                    },
          'end': {
            'date': str_to_date(movie_dates[i])
                }
         
          }


        event = service.events().insert(calendarId='calendarId', body=event).execute()

def str_to_date(date):
    date = date.split(' ')
    if date[3] == 'ENERO':
        return '2020-01-' + date[1]
    if date[3] == 'FEBRERO':
        return '2020-02-' + date[1]
    if date[3] == 'MARZO':
        return '2020-03-' + date[1]
    if date[3] == 'ABRIL':
        return '2020-04-' + date[1]
    if date[3] == 'MAYO':
        return '2020-05-' + date[1]
    if date[3] == 'JUNIO':
        return '2020-06-' + date[1]
    if date[3] == 'JULIO':
        return '2020-07-' + date[1]
    if date[3] == 'AGOSTO':
        return '2020-08-' + date[1]
    if date[3] == 'SEPTIEMBRE':
        return '2020-09-' + date[1]
    if date[3] == 'OCTUBRE':
        return '2020-10-' + date[1]
    if date[3] == 'NOVIEMBRE':
        return '2020-11-' + date[1]
    if date[3] == 'DICIEMBRE':
        return '2020-12-' + date[1]

if __name__ == '__main__':
    main()