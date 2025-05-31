import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver options
options = webdriver.ChromeOptions()
options.add_argument('--log-level=1')


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
]
options.add_argument(f"user-agent={user_agents[randint(0, len(user_agents) - 1)]}")

# Input and output file paths
input_file = 'Controls_links.csv' 
output_file = 'Extra_Details.csv'  


df_links = pd.read_csv(input_file)
urls = df_links['URL'].tolist()

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


HEADING_KEYWORDS = [
    "Responsibilities", "Responsibility", "Qualifications", "Experience", "Accountabilities",
    "Specifications", "Scope", "Need", "Skills", 'Evidence Of', 'Desired', 'Requirements', 'Must Have'
]

# Function to extract text under specific headings
def extract_section_text(soup, heading_keyword):
    """Extracts text under a specific heading"""
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


job_details = []


for url in urls:
    print(f"Processing URL: {url}")

    try:
        # Open the job link
        driver.get(url)
        sleep(randint(5, 12))  

        # Parse page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract job title, company, location
        def extract_text(selector, attr=None):
            """Helper function to extract text with error handling"""
            element = soup.find(selector, class_=attr) if attr else soup.find(selector)
            return element.get_text(strip=True) if element else "Not found"

        job_title = extract_text('h1', 'chakra-heading css-yvgnf2')
        company = extract_text('span', 'chakra-stack css-xyzzkl')
        location = extract_text('span', 'chakra-stack css-xyzzkl')

       
        extracted_sections = {}
        for keyword in HEADING_KEYWORDS:
            section_text = extract_section_text(soup, keyword)
            if section_text:
                extracted_sections[keyword] = section_text

        # Add job metadata
        extracted_sections['URL'] = url
        extracted_sections['Job Title'] = job_title
        extracted_sections['Company'] = company
        extracted_sections['Location'] = location
        extracted_sections['Date Collected'] = pd.Timestamp.today().strftime('%d/%m/%Y')

        # Append extracted details
        job_details.append(extracted_sections)
        print(f"Extracted details for: {job_title}, {company}, {location}")

        # Random sleep before next request
        sleep(randint(15, 45))

    except (NoSuchElementException, TimeoutException, JavascriptException) as e:
        print(f"Error processing URL {url}: {e}")
        continue

# Quit WebDriver
driver.quit()

# Save extracted job details to CSV
df_jobs = pd.DataFrame(job_details)
df_jobs.to_csv(output_file, index=False, mode='a', header=not pd.io.common.file_exists(output_file))

print(f"Scraping completed. Data saved to {output_file}.")
