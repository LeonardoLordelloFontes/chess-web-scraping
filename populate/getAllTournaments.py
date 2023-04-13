from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import mysql.connector

from elo import *

file = open("populate/tournaments2.txt", "w")

s=Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=s)

url = "https://lichess.org/team/circulo-ajedrez-floresta/tournaments"

driver.get(url)

completed_tournaments = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/div/div[2]/div[2]')
headers = completed_tournaments.find_elements(By.CLASS_NAME, "header")

for header in headers:
    element_link = header.find_element(By.TAG_NAME, "a")
    link = element_link.get_attribute("href") + "\n"
    file.write(link)