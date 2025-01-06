import requests
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

import pandas as pd
import numpy as np

import time


finished_matches = pd.DataFrame(columns=[
    'date', 'winning_team', 'losing_team', 'home_team', 'away_team', 'score', 'venue'])
unfinished_matches = pd.DataFrame(columns=[
    'date', 'home_team', 'away_team', 'venue'])

for page_number in range(1, 12):
    link = f'https://www.svleague.jp/en/sv_men/match/list?calender=&league_id%5B%5D=20&pg={page_number}'

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    match_area = soup.find('div', class_='matchArea3')

    if match_area:
        schedule_blocks = match_area.find_all('div', class_='matchScheduleBlock')

        for block in schedule_blocks:
            body = block.find('div', class_='matchScheduleBlockBody')

            date_body = body.find('div', class_='matchScheduleDate')
            year = date_body.find('span', class_='year').text
            date = date_body.find('span', class_='date').text.replace('.', '/')
            time_t = date_body.find('span', class_='time').text
            date_and_time = datetime.strptime(f'{year} {date} {time_t}', '%Y %m/%d %H:%M')

            game_info = body.find('div', class_='gameBox')
            result_box = game_info.find('div', class_='resultBox')
            venue = game_info.find('div', class_='venue').text.strip()

            teamA = result_box.find('div', class_='teamA').text.replace('"', '').strip()
            teamB = result_box.find('div', class_='teamB').text.replace('"', '').strip()
            teamA, teamAhome = teamA.split('\n')
            teamAhome = True if teamAhome == 'HOME' else False
            teamB, teamBhome = teamB.split('\n')
            teamBhome = True if teamBhome == 'HOME' else False
            home_team = teamA if teamAhome else teamB
            away_team = teamA if teamBhome else teamB

            score = result_box.find('div', class_='point').text.strip()

            if score == 'VS':
                unfinished_matches.loc[len(unfinished_matches)] = [date_and_time.strftime('%Y-%m-%dT%H:%M'), home_team, teamB, venue]
            
            else:
                scoreA, scoreB = map(int, score.split('-'))

                teamAwinner = True if scoreA > scoreB else False
                teamBwinner = True if scoreB > scoreA else False
                score = f'{max(scoreA, scoreB)}-{min(scoreA, scoreB)}'

                finished_matches.loc[len(finished_matches)] = [date_and_time.strftime('%Y-%m-%dT%H:%M'), 
                                                              teamA if teamAwinner else teamB, 
                                                              teamA if teamBwinner else teamA, 
                                                              home_team, away_team, score, venue]

    time.sleep(0.5)

print(unfinished_matches['venue'].nunique())
