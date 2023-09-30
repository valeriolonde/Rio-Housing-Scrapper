from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os

class House:
    ## Initializing the House class with its attributes
    def __init__(self, type_of_property, address, region, aluguel, aluguel_total, area, rooms, bathrooms, garage, furnished):
        self.type_of_property = type_of_property
        self.address = address
        self.region = region
        self.aluguel = aluguel
        self.aluguel_total = aluguel_total
        self.area = area
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.garage = garage
        self.furnished = furnished

class HouseScraper:
    ## Initializing the scraper class and its attributes
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.houses = []

    ## Function to extract house details from a string
    def extract_details(self, detail_text):
        size_pattern = r"(\d+) m²"
        rooms_pattern = r"(\d+) quarto"
        bathrooms_pattern = r"(\d+) banheiro"
        garage_pattern = r"(\d+) garagem"

        size = re.search(size_pattern, detail_text)
        rooms = re.search(rooms_pattern, detail_text)
        bathrooms = re.search(bathrooms_pattern, detail_text)
        garage = re.search(garage_pattern, detail_text)
        furnished = "mobiliado" in detail_text

        size = int(size.group(1)) if size else None
        rooms = int(rooms.group(1)) if rooms else None
        bathrooms = int(bathrooms.group(1)) if bathrooms else None
        garage = int(garage.group(1)) if garage else None

        return size, rooms, bathrooms, garage, furnished

    ## Function to scrape house data from the website
    def scrape_houses(self):
        self.driver.get("https://www.quintoandar.com.br/")
        self.driver.implicitly_wait(4)

        city_input = self.driver.find_element(By.XPATH, "//input[@name='landing-city-input']")
        city_input.clear()
        city_input.send_keys("Rio de Janeiro")
        action = ActionChains(self.driver)
        action.move_to_element(city_input).move_by_offset(0, 50).click().perform()

        search_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'sc-fqkvVR') and text()='Buscar imóveis']")
        search_button.click()
        skip_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Pular tudo']]")
        skip_button.click()

        count = 0
        current_houses = 0

        while count < 2500:
            load_more_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'sc-himrzO') and text()='Ver mais']")))
            load_more_button.click()

            houses = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'sc-isijxy-0')]")))

            ## Iterating through the houses to extract data
            for house in houses[current_houses:]:
                type_of_property = house.find_element(By.XPATH, ".//span[@data-testid='house-card-type']/span").text
                address = house.find_element(By.XPATH, ".//span[@data-testid='house-card-address']").text
                region = house.find_element(By.XPATH, ".//span[@data-testid='house-card-region']").text
                aluguel = house.find_element(By.XPATH, ".//span[starts-with(text(), 'Aluguel R$')]").text.replace("Aluguel R$", "").strip()
                aluguel_total = house.find_element(By.XPATH, ".//span[starts-with(text(), 'Total R$')]").text.replace("Total R$", "").strip()
                area_info = house.find_element(By.XPATH, ".//small[@data-testid='house-card-area']").text
                area, rooms, bathrooms, garage, furnished = self.extract_details(area_info)
                house_obj = House(type_of_property, address, region, aluguel, aluguel_total, area, rooms, bathrooms, garage, furnished)
                self.houses.append(house_obj)
                count += 1
                print(f"{count} houses scraped.")
                if count >= 2500:
                    break
            current_houses = len(houses)

        ## Saving the scraped data to a CSV file
        df = pd.DataFrame([house.__dict__ for house in self.houses])
        if os.path.exists('housing_data_2.csv'):
            old_df = pd.read_csv('housing_data_2.csv')
            df = pd.concat([old_df, df]).drop_duplicates().reset_index(drop=True)
        df.to_csv('housing_data_2.csv', index=False)
        self.driver.close()  

if __name__ == "__main__":
    execution_count = 0
    ## Running the scraper multiple times
    for _ in range(3):
        execution_count += 1
        print(f"Scrape number {execution_count} in progress...")
        scraper = HouseScraper()
        scraper.scrape_houses()
