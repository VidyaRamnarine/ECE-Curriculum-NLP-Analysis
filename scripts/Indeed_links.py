import pandas as pd
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# WebDriver options
option = webdriver.ChromeOptions()
option.add_argument('--log-level=1')

# Job Search Details
job = 'Power Systems Engineer'
location = 'Miami'
base_url = 'https://www.indeed.com/jobs?q={}&l={}%2C+FL&from=searchOnHP&vjk=167deac257f8360d&start={}' #https://www.indeed.com/jobs?q=Electrical+and+Computer+Engineering&l=New+York%2C+NY

#Initialize Web Driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

# Lists to store job links
job_links = []

page_limit = 3# Limit to 5 pages max
jobs_per_page = 10 # Indeed uses an offset of 10 per page

# Loop through the pages
for page in range(page_limit):

    # Calculate offset for each page
    start_offset = page * jobs_per_page
    url = base_url.format(job, location, start_offset)
    
    # Load the page
    driver.get(url)

    # Random sleep to mimic human interaction
    sleep(randint(2, 5))  

    # Try to find job listings
    try:
       
        job_page = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'mosaic-jobResults')))
        
        print(f"Page {page + 1}: Job elements loaded.")
        
        links = job_page.find_elements(By.CLASS_NAME, 'job_seen_beacon')

        #job_seen_beacon

        # Extract job links
        for link in links:

            try:
                job_link = link.find_element(By. TAG_NAME, 'a').get_attribute("href")

                sleep(randint(2, 10))

                # Filter for job links (Indeed links contain "clk")
                if job_link and "clk" in job_link:  
                    job_links.append([job_link])
                    print(job_links)
                # Short delay between link retrieval
                sleep(randint(1, 5))  

            except NoSuchElementException:
                
                print("Link not found in a job card.")


            except StaleElementReferenceException:
                print("Stale element encountered; retrying.")
                continue

    except NoSuchElementException:
        print("No more job listings found on this page.")
        break  

# Quit driver after collecting all job links
driver.quit()

# Store in CSV file
df = pd.DataFrame(job_links, columns=['URL'])
df.to_csv('Indeed_Miami_Power.csv')

print("Job links collected: ")
