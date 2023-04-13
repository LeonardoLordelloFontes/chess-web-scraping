from selenium.webdriver.common.by import By
from round import *
from time import sleep

def get_player_id(db_cursor, username):
    query = "SELECT player_id FROM player where username = %s"

    val = (username,)

    db_cursor.execute(query, val)
    result = db_cursor.fetchall()

    return result[0][0]

def get_total_number_of_games(db_cursor, player_id):
    query = "SELECT COUNT(*) FROM game WHERE white_player_id = %s or black_player_id = %s"
    
    val = (player_id, player_id)

    db_cursor.execute(query, val)
    result = db_cursor.fetchall()

    return result[0][0]

def new_player(db_cursor, username):
    new_player = False

    query = "SELECT player_id FROM player WHERE username = %s"

    val = (username,)
    db_cursor.execute(query, val)
    result = db_cursor.fetchall()

    if len(result) == 0:
        new_player = True

    return new_player

def get_players_data(driver):
    players = {}

    next_button = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/div[2]/div[1]/div[2]/div/button[4]')

    usernames = driver.find_elements(By.CLASS_NAME, "name")
    scores = driver.find_elements(By.CLASS_NAME, "pairings")

    for i in range (len(usernames)):
        players[usernames[i].text] = scores[i].text.split("\n")

    while next_button.is_enabled():
        next_button.click()
        sleep(1)
        usernames = driver.find_elements(By.CLASS_NAME, "name")
        scores = driver.find_elements(By.CLASS_NAME, "pairings")

        for i in range (len(usernames)):
            players[usernames[i].text] = scores[i].text.split("\n")

    return players

def insert_elo_new_player(db_cursor, username):
    player_id = get_player_id(db_cursor, username)

    insert = "INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (%s, %s, %s, %s)"
    val = (player_id, "Blitz", 1000, "2023-01-01")
    db_cursor.execute(insert, val)

    insert = "INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (%s, %s, %s, %s)"
    val = (player_id, "Bullet", 1000, "2023-01-01")
    db_cursor.execute(insert, val)

    insert = "INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (%s, %s, %s, %s)"
    val = (player_id, "Rapid", 1000, "2023-01-01")
    db_cursor.execute(insert, val)

    insert = "INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (%s, %s, %s, %s)"
    val = (player_id, "Classical", 1000, "2023-01-01")
    db_cursor.execute(insert, val)

def insert_players_tournament_data(db_cursor, players, tournament_id):
    for player in players:
        player_id = get_player_id(db_cursor, player)

        insert = "INSERT INTO player_tournament (player_id, tournament_id) VALUES (%s, %s)"
        val = (player_id, tournament_id)
        db_cursor.execute(insert, val)

def insert_player_round_data(db_cursor, players, tournament_id, rounds):
    insert = "INSERT INTO player_round (player_id, round_id, score) VALUES (%s, %s, %s)"

    for player in players:
        player_id = get_player_id(db_cursor, player)
        score = 0

        for round in range(1, rounds+1):
            round_id = get_round_id(db_cursor, tournament_id, round)
            score_text = players[player][round-1]

            if score_text == "½":
                score += 0.5

            elif score_text == "-":
                score += 0
            
            else:
                score += float(score_text)

            val = (player_id, round_id, score)

            db_cursor.execute(insert, val)

def insert_players_data(db_cursor, players):
    for player in players:
        if new_player(db_cursor, player):
            
            insert = "INSERT INTO player (username) VALUES (%s)"
            val = (player,)
            db_cursor.execute(insert, val)

            insert_elo_new_player(db_cursor, player)