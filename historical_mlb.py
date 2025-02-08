import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime

historical = pd.DataFrame(columns=['Year', 'Rank', 'Player', 'Position', 'Team', 'Level', 'ETA', 'Current Age', 'Height/Weight', 'Bats', 'Throws'])

for year in range(2011, datetime.datetime.now().year+1):
    if year < datetime.datetime.now().year:
        url = f'https://www.mlb.com/milb/prospects/{year}'
    elif year == datetime.datetime.now().year:
        url = 'https://www.mlb.com/prospects'
    else:
        pass

    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="load-more__button p-button__button p-button__button--regular p-button__button--secondary"]'))).click()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    prospects = soup.find_all('table', 'rankings__table rankings__table--top100')

    data = []
    for table in prospects:
        rows = table.find_all('tr')
        for row in rows:
            rank_td = row.find('td', 'rankings__table__cell--rank')
            player_td = row.find('td', 'rankings__table__cell--player')
            position_td = row.find('td', 'rankings__table__cell--position')
            team_td = row.find('td', 'rankings__table__cell--team')
            level_td = row.find('td', 'rankings__table__cell--level')
            eta_td = row.find('td', 'rankings__table__cell--eta')
            currentAge_td = row.find('td', 'rankings__table__cell--currentAge')
            heightWeight_td = row.find('td', 'rankings__table__cell--heightWeight')
            bats_td = row.find('td', 'rankings__table__cell--bats')
            throws_td = row.find('td', 'rankings__table__cell--throws')
            if rank_td and player_td:
                rank = rank_td.text.strip()
                player = player_td.text.strip()
                position = position_td.text.strip()
                team = team_td.text.strip()
                level = level_td.text.strip()
                if eta_td:
                    eta = eta_td.text.strip()
                else:
                    eta = ''
                currentAge = currentAge_td.text.strip()
                if heightWeight_td:
                    heightWeight = heightWeight_td.text.strip()
                else:
                    heightWeight = 'N/A'
                bats = bats_td.text.strip()
                throws = throws_td.text.strip()
                data.append([year, rank, player, position, team, level, eta, currentAge, heightWeight, bats, throws])
    # Create a DataFrame for the current year and concatenate it with the historical DataFrame
    year_df = pd.DataFrame(data, columns=['Year', 'Rank', 'Player', 'Position', 'Team', 'Level', 'ETA', 'Current Age', 'Height/Weight', 'Bats', 'Throws'])
    historical = pd.concat([historical, year_df], ignore_index=True)

# Print the DataFrame
historical.to_csv('historical_mlb_pipeline.csv', index=False) 
print(historical)
