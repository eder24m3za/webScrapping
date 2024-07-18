from WebDriverManager import WebDriverManager
from GenericScraper import GenericScraper
from Instruccions import transfermarkt_instructions, sofascore_instructions

def main():
    web_driver_manager = WebDriverManager()
    web_driver_manager.setup_driver()

    scraper = GenericScraper(web_driver_manager.driver)
    
    # Ejecutar scraping para Transfermarkt
    scraper.scrape(transfermarkt_instructions)
    
    # Ejecutar scraping para SofaScore
    #scraper.scrape(sofascore_instructions)

    web_driver_manager.close_driver()

if __name__ == '__main__':
    main()
