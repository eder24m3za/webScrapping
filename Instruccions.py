import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def transfermarkt_instructions(driver, data):
    driver.get("https://www.transfermarkt.mx")
    time.sleep(5)
    #accept_button = driver.find_element(By.XPATH, "//button[@aria-label='Aceptar y continuar']")
    #accept_button.click()
    #time.sleep(5)
    search_bar = driver.find_element(By.CLASS_NAME, "tm-header__input--search-field")
    search_bar.send_keys("Santos Laguna")
    search_bar.send_keys(Keys.RETURN)
    
    table = driver.find_element(By.CLASS_NAME, "items")
    links = table.find_elements(By.TAG_NAME, "a")
    
    for a in links:
        if a.get_attribute("title") == "Santos Laguna":
            a.click()
            break
    
    time.sleep(2)
    table_player = driver.find_element(By.CLASS_NAME, "items")
    link_desc = table_player.find_element(By.CSS_SELECTOR, "a.sort-link.desc")
    link_desc.click()
    time.sleep(6)
    #link_asc = table_player.find_element(By.CSS_SELECTOR, "a.sort-link.asc")
    #link_asc.click()
    #time.sleep(2)
    
    table_player = driver.find_element(By.CLASS_NAME, "items")
    tbody_player = table_player.find_element(By.TAG_NAME, "tbody")
    tr_player = tbody_player.find_elements(By.XPATH, "./tr")
    
    for tr in tr_player:
        try:
            posrela = tr.find_element(By.CLASS_NAME, "posrela")
            td_name = posrela.find_element(By.CLASS_NAME, "hauptlink")
            cost = tr.find_element(By.CLASS_NAME, "rechts.hauptlink")
            data.append({"Nombre": td_name.text, "Costo": cost.text})
        except Exception as e:
            print(f"Error inesperado: {e}")

def sofascore_instructions(driver, data):
    driver.get("https://www.sofascore.com")
    form_search = driver.find_element(By.TAG_NAME, "form")
    search_bar = form_search.find_element(By.TAG_NAME, "input")
    search_bar.send_keys("Santos Laguna")
    search_bar.send_keys(Keys.RETURN)
    
    time.sleep(1)
    link_element = driver.find_element(By.CSS_SELECTOR, "a[href='/team/football/santos-laguna/1948']")
    link_element.click()
    time.sleep(5)
    show_more_button = driver.find_element(By.CSS_SELECTOR, "button div.Box span.Text")
    show_more_button.click()
    
    table_player = driver.find_element(By.CLASS_NAME, "Box.idbnlH")
    links = table_player.find_elements(By.TAG_NAME, "a")
    
    for a in links:
        div_span = a.find_element(By.CLASS_NAME, "Box.kUNcqi")
        span = div_span.find_element(By.CLASS_NAME, "Text.ietnEf")
        span_rating = a.find_element(By.CSS_SELECTOR, "span.Text.ietnEf > div.Box > span.Text.lphHQM")
        aria_valuenow = span_rating.get_attribute("aria-valuenow")
        data.append({"Nombre": span.text, "Score": aria_valuenow})
