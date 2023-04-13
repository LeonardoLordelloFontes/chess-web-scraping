from selenium.webdriver.common.by import By

def get_tournament_name(driver):
    name = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/div[2]/div[1]/div[1]/div[1]/h1')
    return name.text

def get_tournament_date(driver):
    element = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/aside/div/time')
    datetime = element.get_attribute("datetime")
    split = datetime.split("T")
    datetime = split[0] + " " + split[1][0:7]
    return datetime

def get_tournament_time_control(driver):
    element = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/aside/div/section/div/p[1]')
    time_control = (element.text.split(" "))[0]
    return time_control

def get_tournament_type_of_time_control(driver):
    type_of_time_control = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/aside/div/section/div/p[1]/span')
    return type_of_time_control.text

def get_tournament_id(mycursor, tournament_name):
    query = "SELECT tournament_id FROM tournament where event_name = %s"
    val = (tournament_name,)

    mycursor.execute(query, val)
    result = mycursor.fetchall()

    return result[0][0]

def insert_tournament_data(mycursor, name, date, time_control, type_of_time_control):

    insert = "INSERT INTO tournament (event_name, event_date, time_control, type_of_time_control) VALUES (%s, %s, %s, %s)"
    val = (name, date, time_control, type_of_time_control)

    mycursor.execute(insert, val)

    tournament_id = get_tournament_id(mycursor, name)

    return tournament_id