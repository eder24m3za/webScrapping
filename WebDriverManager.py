from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        service = Service(executable_path="c:/Users/egmr9/OneDrive/Documentos/9B Python/Practica 4/chrome/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()