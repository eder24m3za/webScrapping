from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd
import pickle
    
def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    transferMark(driver)
    #sofascore(driver)


def transferMark(driver):        
    driver.get("https://www.transfermarkt.mx")
    jsonPlayers = []
    
    time.sleep(5)
    accept_button = driver.find_element(By.XPATH, "//button[@aria-label='Aceptar y continuar']")
    
    accept_button.click()
    time.sleep(5)
    search_bar = driver.find_element(By.CLASS_NAME, "tm-header__input--search-field")
    search_bar.send_keys("Santos Laguna")
    search_bar.send_keys(Keys.RETURN)
    
    # Encontrar el elemento con la clase 'items'
    table = driver.find_element(By.CLASS_NAME, "items")
    # Encontrar todos los enlaces dentro del elemento con la clase 'items'
    links = table.find_elements(By.TAG_NAME, "a")
                
    # Iterar sobre los enlaces y encontrar el que tiene el title 'Santos Laguna'
    for a in links:
        if a.get_attribute("title") == "Santos Laguna":
            a.click()
            print("Found and clicked the element")
            break
    else:
        print("Element not found")
    
    tablePlayer = driver.find_element(By.CLASS_NAME, "items")
    linkDesc = tablePlayer.find_element(By.CSS_SELECTOR, "a.sort-link.desc")
    linkDesc.click()
    time.sleep(5)
    tablePlayer = driver.find_element(By.CLASS_NAME, "items")
    linkAsc = tablePlayer.find_element(By.CSS_SELECTOR, "a.sort-link.asc")
    linkAsc.click()
    time.sleep(2)
        
    tablePlayer = driver.find_element(By.CLASS_NAME, "items")
    tbodyPlayer = tablePlayer.find_element(By.TAG_NAME, "tbody")
    trPlayer = tbodyPlayer.find_elements(By.XPATH, "./tr")
    
    print(len(trPlayer))
    
    for tr in trPlayer:
        try:
            posrela = tr.find_element(By.CLASS_NAME, "posrela")
            tdName = posrela.find_element(By.CLASS_NAME, "hauptlink")
            cost = tr.find_element(By.CLASS_NAME, "rechts.hauptlink")
            jsonPlayers.append({"Nombre": tdName.text, "Costo": cost.text})
            print(tdName.text + " - " + cost.text)
        except Exception as e:
            print(f"Error inesperado: {e}")
            
    # Imprimir el JSON resultante
    driver.close()
    df = pd.DataFrame(jsonPlayers)
    excel_file = 'jugadores.xlsx'

    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"Archivo Excel '{excel_file}' creado exitosamente.")

def sofascore(driver):
    driver.get("https://www.sofascore.com")
    jsonPlayersScore = []
    formSearch = driver.find_element(By.TAG_NAME, "form")
    
    search_bar = formSearch.find_element(By.TAG_NAME, "input")
    search_bar.send_keys("Santos Laguna")
    search_bar.send_keys(Keys.RETURN)
    
    time.sleep(1)
    link_element = driver.find_element(By.CSS_SELECTOR, f"a[href='/team/football/santos-laguna/1948']")
    link_element.click()
    time.sleep(5)
    show_more_button = driver.find_element(By.CSS_SELECTOR, "button div.Box span.Text") 
    
    # Hacer clic en el button encontrado
    show_more_button.click()
    
    tablePlayer = driver.find_element(By.CLASS_NAME, "Box.idbnlH")
    links = tablePlayer.find_elements(By.TAG_NAME, "a")
    
    for a in links:
        divSpan = a.find_element(By.CLASS_NAME, "Box.kUNcqi")
        span = divSpan.find_element(By.CLASS_NAME, "Text.ietnEf")
        
        span_rating = a.find_element(By.CSS_SELECTOR, "span.Text.ietnEf > div.Box > span.Text.lphHQM")
        aria_valuenow = span_rating.get_attribute("aria-valuenow")
        jsonPlayersScore.append({"Nombre": span.text, "Score": aria_valuenow})
    
    driver.close()
    df = pd.DataFrame(jsonPlayersScore)
    
    excel_file = 'jugadoresScore.xlsx'
    
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"Archivo Excel '{excel_file}' creado exitosamente.")
    
    
if __name__ == '__main__':
    main()