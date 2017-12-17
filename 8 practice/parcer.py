# -*- coding: utf-8 -*-
import urllib.request
import re
import datetime
import psycopg2

article_titles = []
usernames = []
publication_dates = []
hubs = []
article_links = []

url = "https://habrahabr.ru/top/monthly/page"
for page in range(1, 11):
    print("Парсим {0} страницу".format(page))
    print(url + str(page))
    try:
        response = urllib.request.urlopen(url+str(page))
    except urllib.error.URLError:
        print('Ошибка: Соединение не установлено, проверьте подключение к '
              'Интернет')
        quit()
    content = response.read().decode(response.headers.get_content_charset())

    regex = '<a.*?>(.+?)</a>\n *</h2>'
    pattern = re.compile(regex)
    article_titles.extend(re.findall(pattern, content))

    regex = '<h2 class=".+?__title">\n *<a href="(.+?)"'
    pattern = re.compile(regex)
    article_links.extend(re.findall(pattern, content))

    # Добавил ИЛИ в регулярку для таких случаев: https://habrahabr.ru/article/342874/,
    # для остальных полей получилось регулярку обобщить.
    regex = r'<span class="user-info__nickname user-info__nickname_small">' \
            r'(.+?)</span>|<a.+?class="preview-data__blog-link">(.+?)</a>'
    pattern = re.compile(regex)
    page_usernames = re.findall(pattern, content)
    # Схлопываем в один список, убираем пустые элементы:
    page_usernames = [item for sublist in page_usernames for item in sublist]
    page_usernames = list(filter(None, page_usernames))
    usernames.extend(page_usernames)

    regex = r'<span class=".+?__tim.+?">(.+?)</span>'
    pattern = re.compile(regex)
    publication_dates.extend(re.findall(pattern, content))

    # Делаем вложенную регулярку, чтобы отсортировать теги по статьям
    regex = r'<ul class=".+?__hubs.+?">(.+?)</ul>'
    pattern = re.compile(regex, flags=re.S)
    hubs_tags = re.findall(pattern, content)
    sorted_hubs = []
    for article_hubs in hubs_tags:
        regex = '<a.*?>(.+?)</a>'
        pattern = re.compile(regex)
        found_hubs = re.findall(pattern, article_hubs)
        # Добавляем список тегов одной статьи к другим:
        sorted_hubs.append(found_hubs)
    hubs.extend(sorted_hubs)

dates_dict = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5,
              'июня': 6, 'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10,
              'ноября': 11, 'декабря': 12}
# Конвертируем русскую дату в числовую:
converted_dates = []
for date in publication_dates:
    if 'сегодня' in date:
        today = str(datetime.datetime.now()).split()[0]
        day = yesterday.split('-')[2]
        converted_month = yesterday.split('-')[1]
    elif 'вчера' in date:
        today = datetime.datetime.now()
        yesterday = str(today - datetime.timedelta(days=1)).split()[0]
        day = yesterday.split('-')[2]
        converted_month = yesterday.split('-')[1]
    else:
        words = date.split()
        day = words[0]
        month = words[1]
        converted_month = dates_dict[month]
    year = '2017'
    converted_date = day+'-'+str(converted_month)+'-'+year
    converted_dates.append(converted_date)

ready_data = list(zip(article_titles, article_links, usernames,
                      converted_dates, hubs))

# Множество уникальных тегов для записи в таблицу тегов:
unique_hubs = [item for sublist in hubs for item in sublist]
unique_hubs = set(unique_hubs)

print("Данные получены, готовится запись в БД:")
pg_password = input("Введите пароль суперпользователя postgres: ")
connect_str = "dbname='postgres' user='postgres' host='localhost' " \
              "password='{0}'".format(pg_password)
try:
    conn = psycopg2.connect(connect_str)
except psycopg2.OperationalError:
    print('Ошибка, введен неправильный пароль или БД postgres не существует')
    quit()

conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute("CREATE DATABASE practice8")
except psycopg2.ProgrammingError:  # Если БД уже создана
    conn.rollback()
    pass
conn.commit()
conn.close()

connect_str = "dbname='practice8' user='postgres' host='localhost' " \
              "password='{0}'".format(pg_password)
try:
    conn = psycopg2.connect(connect_str)
except psycopg2.OperationalError:
    print('Ошибка, БД не существует')
    quit()

cursor = conn.cursor()
try:
    cursor.execute("DROP TABLE data,hubs,data_hubs")
except psycopg2.ProgrammingError:  # Если нечего дропать
    conn.rollback()
    pass

cursor.execute("CREATE TABLE data (id serial PRIMARY KEY, article_title "
               "varchar(130), article_link varchar(60), username varchar(20),"
               "publication_date date);CREATE TABLE hubs (id serial PRIMARY KEY,"
               " hub_name varchar(60)); CREATE TABLE data_hubs (article_id int"
               " REFERENCES data(id), hub_id int REFERENCES hubs(id));")
conn.commit()

for unique_hub in unique_hubs:
    insert_query = "INSERT INTO hubs (hub_name) values ('{0}');".format(unique_hub)
    cursor.execute(insert_query)
conn.commit()

# entry - строка, entry[n] - поле
for article_id, entry in enumerate(ready_data):
    article_id += 1
    insert_query = "INSERT INTO data (article_title, article_link, username, " \
                   "publication_date) values ('{0}','{1}','{2}','{3}');".format(
                    entry[0], entry[1], entry[2], entry[3])
    try:
        cursor.execute(insert_query)
    except psycopg2.ProgrammingError:
        conn.rollback()
        # Убираем кавычку, если она встречается в заголовке статьи:
        fixed_title = entry[0].replace("'", "")
        insert_query = "INSERT INTO data (article_title, article_link, " \
                       "username, publication_date) values ('{0}','{1}','{2}'," \
                       "'{3}');".format(fixed_title, entry[1], entry[2], entry[3])
        cursor.execute(insert_query)

    # Отсортированные теги идут в промежуточную таблицу, по ним ищутся id из
    # таблицы тегов и связываются со статьями:
    for hub in entry[4]:
        insert_query = "INSERT INTO data_hubs (article_id,hub_id) values " \
                       "('{0}',(SELECT id from hubs where hub_name='{1}'))"\
            .format(article_id, hub)
        cursor.execute(insert_query)
    conn.commit()

conn.commit()
conn.close()
print("Запись в БД прошла успешно")
