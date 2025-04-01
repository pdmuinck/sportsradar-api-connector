import requests
import json
import mysql.connector

r = requests.get(url='https://lsc.fn.sportradar.com/sportradar/en/Europe:Berlin/gismo/event_fullfeed/0/24',
                 headers={
                     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})

response=json.loads(r.text)
sports=response['doc'][0]['data']
matches=[]
for sport in sports:
    sport_name=sport['name']
    if(sport_name =='Soccer'):
        categories=sport['realcategories']
        for category in categories:
            tournaments=category['tournaments']
            for tournament in tournaments:
                tournament_name=tournament['name']
                for match in tournament['matches']:
                    match_date=match['_dt']['date']
                    match_time=match['_dt']['time']
                    match_id=match['_id']
                    home_team=match['teams']['home']['name']
                    away_team=match['teams']['away']['name']
                    matches.append([match_id,match_date, match_time, home_team, away_team, tournament_name.strip(), sport_name])

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
cnx.cursor().execute("CREATE DATABASE IF NOT EXISTS sportradar")
cnx.cursor().execute("CREATE TABLE IF NOT EXISTS sportradar.matches(`match_id` INT, `match_date` DATE, `match_time` VARCHAR(20), `home_team` VARCHAR(255), `away_team` VARCHAR(255), `tournament` VARCHAR(255), `sport` VARCHAR(255))")
cnx.cursor().executemany("INSERT INTO sportradar.matches VALUES (%s, %s, %s, %s, %s, %s, %s)", matches)
cnx.commit()
cnx.close()
