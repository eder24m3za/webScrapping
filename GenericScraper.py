import pandas as pd

class GenericScraper:
    def __init__(self, driver):
        self.driver = driver
        self.data = []

    def scrape(self, scraper, instructions):
        scraper.scrape(self.driver, self.data, instructions)
        self.save_to_excel(scraper.__class__.__name__)

    def save_to_excel(self, filename):
        df = pd.DataFrame(self.data)
        df.to_excel(f'{filename}.xlsx', index=False, engine='openpyxl')
        print(f"Archivo Excel '{filename}.xlsx' creado exitosamente.")
