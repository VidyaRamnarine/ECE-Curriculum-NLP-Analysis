import pandas as pd
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException
from bs4 import BeautifulSoup


option = webdriver.ChromeOptions()
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"]
option.add_argument(f"user-agent={user_agents[randint(0, len(user_agents) - 1)]}")
option.add_argument('--log-level=1')

output_file = r'C:\Users\vidya\CaribbeanJobs\Extra_Details.csv'
source = r'C:\Users\vidya\Linkedin\LinkedIn_Extra_Links.csv'


df = pd.read_csv(source, usecols=[0])

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
jobdescriptions = []

HEADING_KEYWORDS = [
    "Responsibilities", "Responsibility", "Qualifications", "Experience", "Accountabilities",
    "Specifications", "Scope", "Need", "Skills", 'Evidence Of', 'Desired', 'Requirements', 'have'
]

# Function to extract text under a specific heading
def extract_section_text(soup, heading_keyword):
    heading = soup.find(lambda tag: tag.name in ['strong', 'p', 'h2', 'h3', 'h4'] and heading_keyword.lower() in tag.text.lower())
    if heading:
        section_text = []
        for sibling in heading.find_next_siblings():
            if sibling.name in ['strong', 'p', 'h2', 'h3', 'h4']:
                sibling_text = sibling.get_text(strip=True).lower()
                if any(keyword.lower() in sibling_text for keyword in HEADING_KEYWORDS):
                    break
                else:
                    continue
            section_text.append(sibling.get_text(strip=True))
        return ' '.join(section_text)
    return None


for rows in df.itertuples():
    pagnation_url = str(rows.URL).strip()
    print(f"Attempting to open URL: {pagnation_url}")

    try:
        driver.get(pagnation_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract all relevant sections dynamically
        extracted_sections = {}
        for keyword in HEADING_KEYWORDS:
            section_text = extract_section_text(soup, keyword)
            if section_text:
                extracted_sections[keyword] = section_text

        if extracted_sections:
            extracted_sections['URL'] = pagnation_url
            pd.DataFrame([extracted_sections]).to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))
            print(f"Processed URL: {pagnation_url}")
            sleep(randint(15, 55))
        else:
            print(f"No relevant sections found for URL: {pagnation_url}")

    except (NoSuchElementException, TimeoutException, JavascriptException) as e:
        print(f"Error on URL {pagnation_url}: {e}")
        continue

driver.quit()
print("Completed processing all URLs.")