import pandas as pd
import json

class GenericScraper:
    def __init__(self, driver):
        self.driver = driver
        self.data = []

    def scrape(self, scraper, instructions, excel='excel'):
        scraper.scrape(self.driver, self.data, instructions)
        self.save_to_excel(excel)

    def save_to_excel(self, filename='excel'):
        df = pd.DataFrame(self.data)
        df.to_excel(f'{filename}.xlsx', index=False, engine='openpyxl')
        print(f"Archivo Excel '{filename}.xlsx' creado exitosamente.")
