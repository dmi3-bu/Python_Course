import urllib.request, json

url = "https://api.football-data.org/v1/competitions"
try:
    response = json.load(urllib.request.urlopen(url))
except urllib.error.URLError:
    print('Ошибка: Соединение не установлено, проверьте подключение к Интернет')
    quit()
print('Топ 5 чемпионатов:')
counter = 1
for championship in response:
    if counter == 6: break
    print(str(counter)+' '+championship['caption'])
    print("Лучшие команды:")
    team_url = url+'/'+str(championship['id'])+'/'+'leagueTable'
    teams_response = json.load(urllib.request.urlopen(team_url))
    teams = teams_response['standing']
    teams.sort(key=lambda team: team['goals'], reverse=True)
    counter2 = 1
    for team in teams:
        if counter2 == 6:
            break
        print(team['teamName']+': '+str(team['goals'])+' голов')
        counter2 += 1
    print()
    counter += 1