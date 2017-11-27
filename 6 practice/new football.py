import urllib.request, json

url = "https://api.football-data.org/v1/competitions"
try:
    response = json.load(urllib.request.urlopen(url))
except urllib.error.URLError:
    print('Ошибка: Соединение не установлено, проверьте подключение к Интернет')
    quit()
print('Топ 5 чемпионатов:')
top_counter = 1
for championship in response[:5]:
    print(str(top_counter)+' '+championship['caption'])
    print("Лучшие команды:")
    team_url = url+'/'+str(championship['id'])+'/'+'leagueTable'
    teams_response = json.load(urllib.request.urlopen(team_url))
    teams = teams_response['standing']
    teams.sort(key=lambda team: team['goals'], reverse=True)
    for team in teams[:5]:
        print(team['teamName']+': '+str(team['goals'])+' голов')
    print()
    top_counter += 1
