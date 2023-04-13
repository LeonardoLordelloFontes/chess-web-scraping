import mysql.connector

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from tournament import *
from player import *
from round import *
from game import insert_game_data
from elo import *

def main():
    file = open("populate/tournaments2.txt", "r")

    s=Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="myusualpasswordhere",
        database="chess"
    )

    for url in file:
        driver.get(url)

        db_cursor = db.cursor()

        tournament_name = get_tournament_name(driver)
        tournament_date = get_tournament_date(driver)
        tournament_time_control = get_tournament_time_control(driver)
        tournament_type_of_time_control = get_tournament_type_of_time_control(driver)
        insert_tournament_data(db_cursor, tournament_name, tournament_date, tournament_time_control, tournament_type_of_time_control)
        tournament_id = get_tournament_id(db_cursor, tournament_name)

        rounds = get_number_of_rounds(driver)
        insert_round_data(db_cursor, tournament_id, rounds)

        players = get_players_data(driver)
        insert_players_data(db_cursor, players)
        insert_players_tournament_data(db_cursor, players, tournament_id)
        insert_player_round_data(db_cursor, players, tournament_id, rounds)

        # games
        insert_game_data(db_cursor, driver, url, tournament_id, rounds)

        #update elo
        update_players_elo(db_cursor, players, tournament_id, tournament_type_of_time_control, tournament_date)

    db.commit()

if __name__ == '__main__':
    main()