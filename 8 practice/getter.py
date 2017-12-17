# -*- coding: utf-8 -*-
import datetime
import psycopg2.extras

pg_password = input("Введите пароль суперпользователя postgres: ")
connect_str = "dbname='practice8' user='postgres' host='localhost' " \
              "password='{0}'".format(pg_password)
try:
    conn = psycopg2.connect(connect_str)
except psycopg2.OperationalError:
    print('Ошибка, введен неправильный пароль или БД с данными не существует')
    quit()
# DictCursor нужен для обращения к полям полученного ответа на запрос:
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


today = str(datetime.datetime.now()).split()[0]
cursor.execute(r'SET datestyle TO "German"')
cursor.execute("SELECT article_title,article_link,username, "
               "publication_date::text from data WHERE publication_date >"
               "'{0}'::timestamp - '7 days'::interval".format(today))
print("\nПопулярные статьи за неделю:")

for row in cursor:
    print(row['article_title'] + ', автор: ' + row['username'] + ', дата: ' +
          str(row['publication_date']) + '\n' + row['article_link'])


cursor.execute('SELECT username,count(*) as article_num FROM data GROUP BY '
               'username HAVING count(*)>1 ORDER BY article_num DESC ')
print("\nСамые активные пользователи:")
for row in cursor:
    print(row['username'] + ' — статей: ' + str(row['article_num']))

cursor.execute('SELECT count(*) as num, hubs.hub_name FROM data_hubs JOIN '
               'hubs on hubs.id = data_hubs.hub_id GROUP BY hub_name '
               'ORDER BY num DESC LIMIT 10')
print("\nСамые популярные теги:")
for row in cursor:
    print(str(row['num']) + ' статей: ' + row['hub_name'])

hub_choice = input("\nВведите тег: ")
date_start = input("Введите дату начала периода в формате 31.12.2017: ")
try:
    date_end = input("Введите дату конца периода: ")
    cursor.execute("SELECT article_title, article_link, publication_date::text,"
                   "hubs.hub_name from data JOIN data_hubs on "
                   "data.id = data_hubs.article_id JOIN hubs on "
                   "data_hubs.hub_id=hubs.id WHERE publication_date>'{0}' and"
                   " publication_date<'{1}' and hub_name = '{2}' ORDER BY "
                   "publication_date".format(date_start, date_end, hub_choice))
except psycopg2.DataError:
    print("Ошибка: Неправильно введена дата!")
    conn.rollback()

if cursor.rowcount <= 0:
    print("\nПо запросу ничего не найдено")
else:
    print("\nПо запросу найдены статьи:")
    for row in cursor:
        print(row['article_title'] + ', дата: ' + str(row['publication_date'])
              + '\n' + row['article_link'])
conn.close()
