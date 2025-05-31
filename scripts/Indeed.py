import pandas as pd
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options
option = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
option.add_argument(f"user-agent={user_agent}") 
option.add_argument('--log-level=1')

# File Paths
output_file = 'Indeed_CE_Miami_details.csv'  # Output file with all job info
source = 'Indeed_CE_Miami_links.csv'    # Input CSV with job URLs C:\Users\vidya\Linkedin\LinkedIn_Canada_description.csv

# Load URLs from CSV file

df = pd.read_csv(source)  # Assuming first column is URLs

# Load already processed URLs to avoid re-processing
try:
    processed_df = pd.read_csv(output_file)
    processed_links = set(processed_df['URL'].tolist())

except FileNotFoundError:
    processed_links = []


# List to store all job details
job_details = []

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)


# Iterate over each URL in the CSV file
for row in df.itertuples():
    job_url = str(row.URL).strip()  # URL' is the column name

    # Skip already processed URLs
    if job_url in processed_links:
        print(f"skipping already processed URL with data: {job_url}")
        continue

    print(f"Processing URL: {job_url}")
    
    try:
        # Open job link
        driver.get(job_url)
        sleep(randint(2, 5))

        # Scroll to load full page content
        for _ in range(randint(3, 5)):
            driver.execute_script("window.scrollBy(0, window.innerHeight / 3);")
            sleep(randint(1, 3))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(randint(1, 3))

        # Scrape job details using BeautifulSoup and Selenium
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Job Title, Company, Location, and Date Posted
        try:
            job_title = soup.find('h1', class_='jobsearch-JobInfoHeader-title').get_text(strip=True) if soup.find('h1', class_='jobsearch-JobInfoHeader-title') else "Job Title not found"
            sleep(randint(2, 15))

            company = soup.find('span', class_='css-1saizt3 e1wnkr790').get_text(strip=True) if soup.find('span', class_='css-1saizt3 e1wnkr790') else "Company not found"
            sleep(randint(1, 15))

            location = soup.find('div', {'id':'jobLocationText'}).get_text(strip=True) if soup.find('div', id='jobLocationText') else "Location not found"
            sleep(randint(3, 10))

            Date_collected = "11/17/2024"
            #date_posted = soup.find('span', class_='posted-time-ago__text').get_text(strip=True) if soup.find('span', class_='posted-time-ago__text') else "Date Posted not found"
        
        except NoSuchElementException as e:
            print("Error retrieving basic job info:", e)
            continue

        # Job Description
        try:
            # Find and expand "See More" button if it exists
            '''see_more_buttons = driver.find_elements(By.XPATH, '//button[contains(@aria-label, "See more")]')
            for button in see_more_buttons:
                driver.execute_script("arguments[0].click();", button)
                sleep(1)  # Allow a bit of time for expansion'''
            
            # Reload page source and parse again for updated content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            description_block = soup.find('div', id = 'jobDescriptionText')
            description_text = description_block.get_text(separator=' ', strip=True) if description_block else "Description not available"
            sleep(randint(2, 10))

        except (NoSuchElementException, JavascriptException) as e:
            print(f"Error retrieving job description: {e}")
            description_text = "Description not found"

        # Add the job data to the list
        job_details.append({
            'URL': job_url,
            'Job Title': job_title,
            'Company': company,
            'Location': location,
            'Date Posted': Date_collected,
            'Description': description_text})

        print(f"Job added: {job_title}, {company}, {location}, {Date_collected}")

        # Add to processed links set
        processed_links.add(job_url)

        # Random wait to mimic human behavior
        sleep(randint(10, 30))

    except (NoSuchElementException, TimeoutException, JavascriptException) as e:
        print(f"Error on URL {job_url}: {e}")
        continue

# Quit driver after processing all URLs
driver.quit()

# Save all job details to CSV after processing all URLs
df_jobs = pd.DataFrame(job_details)
df_jobs.to_csv(output_file, index=False, mode= 'a')
#df_jobs.to_csv(output_file, index=False, mode='a', header=not processed_links)

print("Completed processing all URLs.")

# Append new jobs to the processed file
'''if not df_jobs.empty:
    # Combine with existing processed data if any
    combined_df = pd.concat([processed_df, df_jobs]).drop_duplicates(subset='URL', keep='last')
    combined_df.to_csv(output_file, index=False)
    print("Updated CSV with new job details.")
else:
    print("No new job details to add.")'''
