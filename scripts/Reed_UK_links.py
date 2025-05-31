import pandas as pd
import time
from time import sleep
from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Setup WebDriver options
option = webdriver.ChromeOptions()
option.add_argument('--log-level=1')

# Job Search Details
job = 'Control+System+Engineer'
location = 'London'

base_url ='https://www.reed.co.uk/jobs/electronics-jobs' 

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)


job_links = []


for page in range(1, 2):
    print(f"Scraping page {page}...")

    # Load the page URL
    driver.get(base_url.format(job, location, page))

    # Ensure page is fully loaded
    sleep(randint(3, 6))

    try:
        # Locate all job result titles
        job_titles = driver.find_elements(By.CLASS_NAME, 'job-card_jobResultHeading__title__IQ8iT')

        for title in job_titles:
            try:
                # Extract the <a> tag inside the job title element
                job_link_element = title.find_element(By.TAG_NAME, 'a')
                job_link = job_link_element.get_attribute("href")
                job_links.append(job_link)
                sleep(randint(1, 5))  # Random sleep to mimic human behavior

            except (NoSuchElementException, StaleElementReferenceException):
                print("Error locating or retrieving link; skipping...")
                continue

    except NoSuchElementException:
        print("No job result titles found on this page.")

# Quit the driver after all links are collected
driver.quit()

# Display collected job links
print(f"Total job links collected: {len(job_links)}")
print(job_links)

# Save links to a CSV file
df = pd.DataFrame(job_links, columns=["URL"])
df.to_csv('Controls_links.csv', mode='a', index=False)
