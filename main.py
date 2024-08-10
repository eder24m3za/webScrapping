import json
from WebDriverManager import WebDriverManager
from GenericScraper import GenericScraper
from ScraperInterface import ScraperInterface

def load_instructions(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    web_driver_manager = WebDriverManager()
    web_driver_manager.setup_driver()

    instructions = load_instructions('Instructions.json')['instructions']

    for site_instructions in instructions:
        for site, actions in site_instructions.items():
            print(f"Scraping {site}...")
            scraper = GenericScraper(web_driver_manager.driver)
            site_scraper = ScraperInterface()
            scraper.scrape(site_scraper, actions)

    web_driver_manager.close_driver()

if __name__ == '__main__':
    main()
