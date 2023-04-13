from player import get_player_id
from math import pow

def get_old_player_rating(db_cursor, player_id, type_of_time_control):

    if type_of_time_control == "Blitz":
        query = "SELECT elo_blitz FROM player WHERE player_id = %s"
    
    elif type_of_time_control == "Rapid":
        query = "SELECT elo_rapid FROM player WHERE player_id = %s"

    elif type_of_time_control == "Bullet":
        query = "SELECT elo_bullet FROM player WHERE player_id = %s"
    
    elif type_of_time_control == "Classical":
        update = "SELECT elo_classical FROM player WHERE player_id = %s"

    val = (player_id,)
    db_cursor.execute(query, val)
    result = db_cursor.fetchall()

    return result[0][0]

def get_player_result(db_cursor, player_id, tournament_id):
    result = 0

    query_white = "SELECT result FROM game WHERE white_player_id = %s and tournament_id = %s"
    query_black = "SELECT result FROM game WHERE black_player_id = %s and tournament_id = %s"

    val = (player_id, tournament_id)
    db_cursor.execute(query_white, val)
    result_white = db_cursor.fetchall()

    db_cursor.execute(query_black, val)
    result_black = db_cursor.fetchall()

    for r in result_white:
        if r[0] == "1 - 0":
            result += 1
        
        elif r[0] == "1/2 - 1/2":
            result += 0.5

    for r in result_black:
        if r[0] == "0 - 1":
            result += 1
        
        elif r[0] == "1/2 - 1/2":
            result += 0.5

    return result

def get_match_expectation(player_rating, opponent_rating):
    return 1/(1 + pow(10,(opponent_rating-player_rating)/400))

def get_player_expectation(db_cursor, player_id, tournament_id, elos):
    expectation = 0

    query = "SELECT black_player_id FROM game where white_player_id = %s and tournament_id = %s UNION SELECT white_player_id FROM game where black_player_id = %s and tournament_id = %s"
    
    val = (player_id, tournament_id, player_id, tournament_id)
    db_cursor.execute(query, val)
    opponents_id = db_cursor.fetchall()

    for opponent_id in opponents_id:
        opponent_rating = elos[opponent_id[0]]
        expectation += get_match_expectation(elos[player_id], opponent_rating)
    
    return expectation

def update_players_elo(db_cursor, players, tournament_id, tournament_type_of_time_control, tournament_date):
    elos = {}

    for player in players:
        player_id = get_player_id(db_cursor, player)
        elos[player_id] = get_old_player_rating(db_cursor, player_id, tournament_type_of_time_control)

    k = 32
    for player_id in elos:
        old_player_rating = get_old_player_rating(db_cursor, player_id, tournament_type_of_time_control)
        player_result = get_player_result(db_cursor, player_id, tournament_id)
        player_expectation = get_player_expectation(db_cursor, player_id, tournament_id, elos)
        new_player_rating = old_player_rating + k * (player_result - player_expectation)

        insert = "INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (%s, %s, %s, %s)"
        
        val = (player_id, tournament_type_of_time_control, new_player_rating, tournament_date)
        db_cursor.execute(insert, val)

        if tournament_type_of_time_control == "Blitz":
            update = "UPDATE player SET elo_blitz = %s WHERE player_id = %s"
        
        elif tournament_type_of_time_control == "Rapid":
            update = "UPDATE player SET elo_rapid = %s WHERE player_id = %s"

        elif tournament_type_of_time_control == "Bullet":
            update = "UPDATE player SET elo_bullet = %s WHERE player_id = %s"
        
        elif tournament_type_of_time_control == "Classical":
            update = "UPDATE player SET elo_classical = %s WHERE player_id = %s"
        
        val = (new_player_rating, player_id)
        db_cursor.execute(update, val)
        