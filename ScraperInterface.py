import time
from selenium.webdriver.common.by import By

class ScraperInterface:
    def scrape(self, driver, data, instructions):
        self.execute_instructions(driver, data, instructions)

    def execute_instructions(self, driver, data, instructions):
        for instruction in instructions:
            action = instruction.get("action")
            if action == "get":
                driver.get(instruction["url"])
            elif action == "click":
                element = self.find_element(driver, instruction["selector"])
                if element:
                    element.click()
            elif action == "write":
                element = self.find_element(driver, instruction["selector"])
                if element:
                    element.send_keys(instruction["text"])
            elif action == "extract":
                self.extract_data(driver, instruction)
            elif action == "back":
                driver.back()  
            time.sleep(instruction.get("wait", 5))

    def find_element(self, driver, selector):
        by = selector.get("by")
        value = selector.get("value")
        try:
            if by == "xpath":
                return driver.find_element(By.XPATH, value)
            elif by == "css":
                return driver.find_element(By.CSS_SELECTOR, value)
            elif by == "class":
                return driver.find_element(By.CLASS_NAME, value)
            elif by == "tag":
                return driver.find_element(By.TAG_NAME, value)
            elif by == "name":
                return driver.find_element(By.NAME, value)
        except Exception as e:
            print(f"Error finding element: {e}")
            return None

    def extract_data(self, driver, instruction):
        print("extracting data")
        table = instruction["table"]
        row_selector = instruction["row"]
        cell_selectors = instruction["cells"]
        excel_filename = instruction.get("excel", "default")  # Obtiene el nombre del archivo Excel

        # Encuentra el contenedor usando el selector proporcionado
        container = self.find_element(driver, table)
        if not container:
            print("Container element not found")
            return

        # Encuentra todas las filas en el contenedor
        rows = container.find_elements(By.XPATH, row_selector)
        print("container " + container.text)
        print("rows " + str(len(rows)))

        data = []
        for row in rows:
            row_data = {}
            valid_row = True

            for cell in cell_selectors:
                try:
                    # Determina el tipo de selector y encuentra el elemento correspondiente
                    selector_type = cell.get("by", "xpath").lower()
                    cell_element = None

                    if selector_type == "xpath":
                        cell_element = row.find_element(By.XPATH, cell["selector"])
                    elif selector_type == "css":
                        cell_element = row.find_element(By.CSS_SELECTOR, cell["selector"])
                    elif selector_type == "tag":
                        cell_element = row.find_element(By.TAG_NAME, cell["selector"])
                    elif selector_type == "class":
                        cell_element = row.find_element(By.CLASS_NAME, cell["selector"])
                    elif selector_type == "name":
                        cell_element = row.find_element(By.NAME, cell["selector"])
                    else:
                        print(f"Unknown selector type: {selector_type}")
                        valid_row = False
                        continue

                    # Si el selector contiene 'attribute', extrae el atributo en lugar del texto
                    if "attribute" in cell:
                        cell_value = cell_element.get_attribute(cell["attribute"]).strip()
                        if not cell_value:
                            print(f"Cell {cell['name']} attribute {cell['attribute']} is empty or not found")
                            valid_row = False
                        row_data[cell["name"]] = cell_value
                    else:
                        cell_text = cell_element.text.strip()
                        if not cell_text:
                            print(f"Cell {cell['name']} is empty or not found")
                            valid_row = False
                        row_data[cell["name"]] = cell_text
                        
                except Exception as e:
                    print(f"Error extracting data for cell {cell['name']}: {e}")
                    valid_row = False
                    row_data[cell["name"]] = None

            if valid_row:
                data.append(row_data)
            else:
                print("Skipping row due to missing or empty cells")

        print("data " + str(data))
        # Guardar los datos en un archivo Excel específico para esta extracción
        self.save_to_excel(excel_filename, data)

    def save_to_excel(self, filename='default', data=[]):
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_excel(f'{filename}.xlsx', index=False, engine='openpyxl')
        print(f"Archivo Excel '{filename}.xlsx' creado exitosamente.")
