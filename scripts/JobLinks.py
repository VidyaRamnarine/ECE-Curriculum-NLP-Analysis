
import pandas as pd
import csv

import time
from time import sleep

from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

#Allow searches 
from selenium.webdriver.common.by import By


#locate elements on webpafe and throw error if it does not exist 
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

#wait times  
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
option.add_argument('--log-level=1')

start = time.time()

#Job Search Details
job = 'Power+Engineering'
location = 'Toronto'

pagnation_url = 'https://ca.linkedin.com/jobs/search?keywords={}&location={}&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

#Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
driver.get(pagnation_url.format(job, location))

#ensure page is loaded
sleep(randint(2, 5))

#get the number of job listings
'''try:
    jobcount_text = driver.find_element(By.CLASS_NAME, 'results-context-header__job-count').text
    no_listings = int(jobcount_text.split(' ')[0])
    print(f'number of job listings: {no_listings}')
except NoSuchElementException:
    print('job count element not found')
    no_listings = 0'''

#creating empty lists to store job info.
job_links = []
job_list = []



try:
    job_page = driver.find_element(By.ID, 'main-content')
    links = job_page.find_elements(By.TAG_NAME, 'a')

    for link in links:
        try:
            job_link = link.get_attribute("href")
            if job_link and "linkedin.com/jobs/view" in job_link:  # Filter out only job links
                job_links.append([job_link])
            time.sleep(randint(1, 3))  # Use shorter sleep to avoid detection

        except StaleElementReferenceException:
            print("Stale element encountered; retrying.")
            continue  # Move to the next link if there's a stale element error

except NoSuchElementException:
    print("Job page or links not found")

# Quit the driver after all links are collected
driver.quit()


'''#collect Job Links
for jj in links:
    job_link = jj.get_attribute("href")
    sleep(randint(10, 20))
    job_description.append([job_link])
  
driver.quit()'''

end = time.time()

#used for CE_Trinidad only
#del job_description[0::2]   

print("Job links collected: ", job_links)  

#Store in CSV file
df = pd.DataFrame(job_links)
df.to_csv('Toronto_Power_links.csv', mode = 'a')

