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

url = 'https://www.mlb.com/prospects'
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
            eta = eta_td.text.strip()
            currentAge = currentAge_td.text.strip()
            heightWeight = heightWeight_td.text.strip()
            bats = bats_td.text.strip()
            throws = throws_td.text.strip()
            data.append([rank, player, position, team, level, eta, currentAge, heightWeight, bats, throws])

# Create a DataFrame
df = pd.DataFrame(data, columns=['Rank', 'Player', 'Position', 'Team', 'Level', 'ETA', 'Current Age', 'Height/Weight', 'Bats', 'Throws'])

# Print the DataFrame
print(df)
