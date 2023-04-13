from selenium.webdriver.common.by import By

def get_number_of_rounds(driver):
    element = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/aside/div/section[1]/div/p[2]/span')
    rounds = int((element.text.split("/"))[0])
    return rounds

def get_round_id(db_cursor, tournament_id, round_number):
    query = "SELECT round_id FROM round where (tournament_id, round_number) = (%s, %s)"
    val = (tournament_id, round_number)

    db_cursor.execute(query, val)
    result = db_cursor.fetchall()

    return result[0][0]

def insert_round_data(db_cursor, tournament_id, rounds):

    insert = "INSERT INTO round (tournament_id, round_number) VALUES (%s, %s)"

    for round_number in range(1, rounds+1):
        val = (tournament_id, round_number)
        db_cursor.execute(insert, val)