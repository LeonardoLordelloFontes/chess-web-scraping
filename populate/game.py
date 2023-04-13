from selenium.webdriver.common.by import By
from player import get_player_id
from round import get_round_id
from time import sleep

def get_data_from_round(driver, url, round_number):
    round_url = url + "/round/" + str(round_number)
    driver.get(round_url)
    data = driver.find_elements(By.CLASS_NAME, 'paginated') 
    return data

def insert_game_data(db_cursor, driver, url, tournament_id, rounds):

    for round in range(1, rounds+1):
        for game in get_data_from_round(driver, url, round):
            info = game.text.split(" ")
            game_link = "lichess.org/" + info[0][1:]
            white_username = info[1]
            result = info[2] + " - " + info[3]
            black_username = info[4]

            white_player_id = get_player_id(db_cursor, white_username)
            black_player_id = get_player_id(db_cursor, black_username)

            round_id = get_round_id(db_cursor, tournament_id, round)

            insert = "INSERT INTO game (round_id, white_player_id, black_player_id, tournament_id, result, game_link) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (round_id, white_player_id, black_player_id, tournament_id, result, game_link)

            db_cursor.execute(insert, val)