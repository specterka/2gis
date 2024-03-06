import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Load URLs from a CSV file
csv_file = 'urls.csv'
df = pd.read_csv(csv_file)

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Make sure to add a new column for scraped content if it doesn't exist
if 'scraped_content' not in df.columns:
    df['scraped_content'] = pd.Series(dtype='str')

for index, row in df.iterrows():
    url = row['links']  # Assuming the column name is 'links'
    try:
        # Open the URL
        driver.get(url)

        # Wait for the dynamic content to load
        time.sleep(2)  # Adjust timing as necessary

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the specific meta tag
        meta_tag = soup.find('meta', attrs={'name': 'description'})

        # Check if the meta tag was found and store the content
        if meta_tag:
            content = meta_tag.get('content')
            df.at[index, 'scraped_content'] = content
        else:
            df.at[index, 'scraped_content'] = 'Content not found'

    except Exception as e:
        print(f'An error occurred while processing {url}: {e}')
        df.at[index, 'scraped_content'] = 'Error occurred'

    # Save the DataFrame to CSV after each URL to ensure data is saved instantly
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

# Don't forget to quit the driver
driver.quit()
