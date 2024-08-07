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
                element.click()
            elif action == "write":
                element = self.find_element(driver, instruction["selector"])
                element.send_keys(instruction["text"])
            elif action == "extract":
                self.extract_data(driver, data, instruction)
            time.sleep(instruction.get("wait", 5))

    def find_element(self, driver, selector):
        by = selector.get("by")
        value = selector.get("value")
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

    def extract_data(self, driver, data, instruction):
        print("extracting data")
        table_selector = instruction["table"]
        row_selector = instruction["row"]
        cell_selectors = instruction["cells"]

        table = self.find_element(driver, table_selector)
        rows = table.find_elements(By.XPATH, row_selector)
        
        print("table " + table.text)
        print("rows " + str(len(rows)))

        for row in rows:
            row_data = {}
            for cell in cell_selectors:
                cell_element = row.find_element(By.XPATH, cell["selector"])
                row_data[cell["name"]] = cell_element.text
                print("element " + cell_element.text)
            data.append(row_data)
