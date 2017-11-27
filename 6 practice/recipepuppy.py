import urllib.request, json

ingredients = input("Введите ингредиенты через пробел на английском:")
ingredients = ingredients.split(" ")
dish = input("Введите тип блюда на английском:")
url = "http://www.recipepuppy.com/api/?i="
for ingredient in ingredients:
    url = url+ingredient+','
url=url.rstrip(',')
url=url+"&q="+dish
page_number = 1
next_page = True
while next_page:
    page_url=url+"&p="+str(page_number)
    try:
        response = json.load(urllib.request.urlopen(page_url))
    except urllib.error.URLError:
        print('Ошибка: Соединение не установлено, проверьте подключение к Интернет')
        quit()
    response = response['results']
    if not response:
        print('Ничего не найдено')
        quit()
    for recipe in response:
        recipe['title'] = recipe['title'].strip('\n')
        print("Название рецепта: "+recipe['title'])
        print("Ингредиенты: " + recipe['ingredients'])
        print("Ссылка на рецепт: " + recipe['href'])
    choice = input("Показать еще рецепты?(y): ")
    if choice == "y":
        page_number += 1
        continue
    else:
        break



