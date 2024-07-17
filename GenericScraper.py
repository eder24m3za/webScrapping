import pandas as pd

class GenericScraper:
    def __init__(self, driver):
        self.driver = driver
        self.data = []

    def scrape(self, instructions):
        instructions(self.driver, self.data)
        self.save_to_excel()

    def save_to_excel(self, filename='data.xlsx'):
        df = pd.DataFrame(self.data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Archivo Excel '{filename}' creado exitosamente.")
    
    def execute_instructions(self, instructions):
        for action in instructions['instructions']:
            if 'url' in action:
                self.driver.get(action['url'])