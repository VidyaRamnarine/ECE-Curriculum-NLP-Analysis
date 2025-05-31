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
job = 'Controls+Engineer'
location = '124'

pagination_url = 'https://www.caribbeanjobs.com/ShowResults.aspx?Keywords={}&autosuggestEndpoint=%2Fautosuggest&Category=&Recruiter=Company&Recruiter=Agency&page={}'

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

# Create a list to store job links
job_links = []

# Loop through the first 5 pages
for page_num in range(1, 3):
    driver.get(pagination_url.format(job, page_num))
    sleep(randint(3, 5))  # Wait for the page to load
    
    try:
        # Locate all job result titles
        job_titles = driver.find_elements(By.CLASS_NAME, 'job-result-title')

        for title in job_titles:
            try:
                # Extract the <a> tag inside the <h2> element
                job_link_element = title.find_element(By.TAG_NAME, 'a')
                job_link = job_link_element.get_attribute("href")
                job_links.append([job_link])
                sleep(randint(1, 3))  # Random sleep to mimic human behavior

            except (NoSuchElementException, StaleElementReferenceException):
                print("Error locating or retrieving link; skipping...")
                continue

    except NoSuchElementException:
        print("No job result titles found on page", page_num)

# Quit the driver after all links are collected
driver.quit()

# Display collected job links
print("Job links collected: ", job_links)

# Save links to a CSV file
df = pd.DataFrame(job_links, columns=["Job Link"])
df.to_csv('Controls_links.csv', mode='a', index=False)

