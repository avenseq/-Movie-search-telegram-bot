from asyncio import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
headers = {'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
           }
# url = 'https://www.kinoafisha.info/rating/movies/'
# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html', 'w') as file: #Сохроняем код в файл, чтобы не грузить сайт запросами
#     file.write(src)
#     #Далее все остальное не нужно - комментируем...


# with sq.connect("data_films.db") as con:
#      cur = con.cursor()
#      cur.execute('''DROP TABLE ifilms''')
#      cur.execute("""CREATE TABLE ifilms (
#      film_id INTEGER PRIMARY KEY,
#      name TEXT,
#      year of issue INTEGER,
#      duration TEXT,
#      href TEXT,
#      contry TEXT,
#      about TEXT,
#      rate TEXT,
#      genre TEXT)""")
# with sq.connect("data_films.db") as con:
#       cur = con.cursor()
#       cur.execute('''ALTER TABLE ifilms
#                     ADD COLUMN genre TEXT;''')
#




# with open('index.html') as file:
#        src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')                                     #Код только для первой страницы
# all_films_href = soup.find_all(class_ = 'movieItem_title')
# with sq.connect("data_films.db") as con:
#     cur = con.cursor()
    # for item in all_films_href:
    #     item_text = item.text.replace(' ', '_').replace(':', '').replace(',', '_')
    #     item_href = item.get('href')
    #     print(f'{item_text}: {item_href}')
    #     req = requests.get(item_href)
    #     srcc = req.text
    #     soup_film = BeautifulSoup(srcc, 'lxml')
    #     film_info = soup_film.find_all(class_='filmInfo_infoData')
    #     duration = film_info[0].text.replace(' ', '_')
    #     print(duration)
    #     year_of_issue = int(film_info[1].text)
    #     cur.execute( f'''INSERT INTO ifilms (name, year, duration, href) VALUES('{item_text}', '{year_of_issue}', '{duration}', '{item_href}')''')
count = 700
with sq.connect("data_films.db") as con:
    cur = con.cursor()
    for i in range(0, 7):
        url = f'https://www.kinoafisha.info/rating/movies/?page={i}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        all_films_href = soup.find_all(class_ = 'movieItem_title')
        for item in all_films_href:
            item_text = item.text
            item_href = item.get('href')

            reqq = requests.get(item_href)
            srcc = reqq.text
            soup_film = BeautifulSoup(srcc, 'lxml')

            film_info = soup_film.find_all(class_ ='filmInfo_infoData')
            duration = film_info[0].text
            year_of_issue = film_info[1].text

            contry_film = soup_film.find(class_ = 'trailer_year')
            if len(contry_film.text.split('/')) == 1:
                contry = '-'
            else:
                contry = contry_film.text.split('/')[1]

            about_film = soup_film.find(class_ = 'visualEditorInsertion filmDesc_editor more_content')
            if about_film == None:
                about = '-'
            else:
                about = about_film.text.replace("'", '_').replace('"', '_')

            rate_film = soup_film.find(class_ = 'rating_imdb imdbRatingPlugin')
            if rate_film == None:
                rate = '-'
            else:
                rate = rate_film.text.replace("'", '_').replace('"', '_')

            genre_film = soup_film.find_all(class_ = 'filmInfo_genreItem button-main')
            genre = "_".join([i.text for i in genre_film])
            print(item_text)
            cur.execute(f'''INSERT INTO ifilms (name, year, duration, href, contry, about, rate, genre) VALUES('{item_text}', '{year_of_issue}', '{duration}', '{item_href}', '{contry}', '{about}', '{rate}', '{genre}')''')
            count-=1

            print(f'Успешно! Еще {count} раз')





