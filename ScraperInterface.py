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
                self.extract_data(driver, data, instruction)
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

    def extract_data(self, driver, data, instruction):
        print("extracting data")
        table_selector = instruction["table"]
        row_selector = instruction["row"]
        cell_selectors = instruction["cells"]

        # Encuentra la tabla usando el selector proporcionado
        table = self.find_element(driver, table_selector)
        if not table:
            print("Table element not found")
            return

        # Encuentra todas las filas en la tabla
        rows = table.find_elements(By.XPATH, row_selector)
        
        for row in rows:
            row_data = {}
            valid_row = True

            for cell in cell_selectors:
                try:
                    # Encuentra la celda usando el selector proporcionado
                    cell_element = row.find_element(By.XPATH, cell["selector"])
                    cell_text = cell_element.text.strip()
                    
                    if cell.get("attribute"):
                        cell_value = cell_element.get_attribute(cell["attribute"]).strip()
                        if not cell_value:
                            print(f"Cell {cell['name']} attribute {cell['attribute']} is empty or not found")
                            valid_row = False
                        row_data[cell["name"]] = cell_value
                    else:
                        if not cell_text:
                            print(f"Cell {cell['name']} is empty or not found")
                            valid_row = False
                        row_data[cell["name"]] = cell_text
                    
                except Exception as e:
                    print(f"Error extracting data for cell {cell['name']}: {e}")
                    # Si ocurre un error al encontrar la celda, marca la fila como inválida
                    valid_row = False
                    row_data[cell["name"]] = None

            # Solo agrega la fila a los datos si todas las celdas se han encontrado
            if valid_row:
                data.append(row_data)
            else:
                print("Skipping row due to missing or empty cells")

        print("data " + str(data))
