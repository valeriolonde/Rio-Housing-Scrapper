# Rio Housing Scraper

This project is designed to scrape house rental listings from the website [quintoandar.com.br](https://www.quintoandar.com.br) using the Selenium library in Python. The [main script](https://github.com/valeriolonde/Rio-Housing-Scrapper/blob/main/quinto_andar.py) automates the browser to interact with the website and extract detailed information on available rental listings in Rio de Janeiro.

## Imports and Dependencies

Essential libraries such as `selenium` for web scraping, `pandas` for data manipulation, `re` for regular expressions, and `os` for interacting with the operating system are imported at the beginning.

## House Class

The `House` class serves as a data model for housing listings. It encompasses attributes like:
- Type of property
- Address
- Region
- Rent amount
- Total rent
- Area (in sq meters)
- Number of rooms
- Number of bathrooms
- Garage spaces
- Furnishing status

## HouseScraper Class

This is the primary class responsible for the scraping process. Key functionalities include:

- `__init__` method: Initializes the web driver and an empty list to store house data.
  
- `extract_details` method: Employs regular expressions to parse essential details about the house from a given text.
  
- `scrape_houses` method: Orchestrates the scraping sequence:
  - Navigates to the website.
  - Inputs "Rio de Janeiro" into the city search field.
  - Clicks the search button and manages any pop-ups or overlays.
  - Iteratively loads and captures house listings up to a predetermined count (2500 in this case). During each iteration, it extracts details like property type, address, region, rent amount, total rent, and other features.
  - Post-scraping, the data is saved to a DataFrame and subsequently exported to a CSV file. If an existing CSV is detected, the new data is appended, and any duplicates are eliminated.

## Execution Logic

At the tail end of the script, there's a segment that instantiates the `HouseScraper` class and triggers the `scrape_houses` method three times. This repetition ensures comprehensive data collection.

