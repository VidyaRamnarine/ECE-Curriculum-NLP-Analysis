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

# Random user-agent selection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
]
options.add_argument(f"user-agent={user_agents[randint(0, len(user_agents) - 1)]}")


input_file = 'Controls_links.csv'  
output_file = 'Extra_Details.csv'  

df_links = pd.read_csv(input_file)
urls = df_links['URL'].tolist()

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Keywords for specific job sections
HEADING_KEYWORDS = [
    "Responsibilities", "Responsibility", "Qualifications", "Experience", "Accountabilities",
    "Specifications", "Scope", "Need", "Skills", 'Evidence Of', 'Desired', 'Requirements', 'Must Have', "opportunity", 
    "need to have", "experience", " be doing", "Expereiences", "Essential"
]

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
        driver.get(url)
        sleep(randint(5, 12))  # Randomized sleep to mimic human behavior
        soup = BeautifulSoup(driver.page_source, 'html.parser')

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

        extracted_sections['URL'] = url
        extracted_sections['Job Title'] = job_title
        extracted_sections['Company'] = company
        extracted_sections['Location'] = location
        extracted_sections['Date Collected'] = pd.Timestamp.today().strftime('%d/%m/%Y')

        job_details.append(extracted_sections)
        sleep(randint(15, 45))  # More random sleep time

    except (NoSuchElementException, TimeoutException, JavascriptException) as e:
        print(f"Error processing URL {url}: {e}")
        continue

driver.quit()

df_jobs = pd.DataFrame(job_details)
df_jobs.to_csv(output_file, index=False, mode='a', header=not pd.io.common.file_exists(output_file))

print(f"Scraping completed. Data saved to {output_file}.")



'''import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver options
options = webdriver.ChromeOptions()
options.add_argument('--log-level=1')

# Input and output file paths
input_file = 'ReedUK_Unrelated_London_links.csv'  # CSV file with job URLs
output_file = 'Unrelated_London_Job_Details.csv'  # Output file to save job details

# Load URLs from the input CSV file
df_links = pd.read_csv(input_file)
urls = df_links['URL'].tolist()

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# List to store job details
job_details = []

# Iterate through the URLs
for url in urls:
    print(f"Processing URL: {url}")
    try:
        # Open the job link
        driver.get(url)
        sleep(randint(2, 10))  # Random delay to mimic human behavior

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract job details
        job_title = (
            soup.find('meta', {'itemprop': 'title'}).get_text(strip=True)
            if soup.find('meta', {'itemprop': 'title'}) else "Job Title not found"
        )
        sleep(randint(5,15))

        company = (
            soup.find('span', {'data-page-component': 'job_description', 'itemprop': 'name'}).get_text(strip=True)
            if soup.find('span', {'data-page-component': 'job_description', 'itemprop': 'name'}) else "Company not found"
        )

        sleep(randint(2, 10))

        location = (
            soup.find('span', {'data-qa': 'regionMobileLbl'}).get_text(strip=True)
            if soup.find('span', {'data-qa': 'regionMobileLbl'}) else "Location not found"
        )

        sleep(randint(2, 10))

        description = (
            soup.find('div', class_='description').get_text(strip=True)
            if soup.find('div', class_='description') else "Description not available"
        )
        sleep(randint(5, 10))

        date =  (
            soup.find('meta', {'itemprop': 'datePosted'}).get_text(strip=True)
            if soup.find('meta', {'itemprop': 'datePosted'}) else "Description not available"
        )
        sleep(randint(2, 8))
        
        

        # Append job details
        job_details.append({
            'URL': url,
            'Job Title': job_title,
            'Company': company,
            'Location': location,
            'Date Collected': date, 
            'Description': description
        })

        print(f"Job added: {job_title}, {company}, {location}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        continue

# Quit the driver
driver.quit()

# Save job details to the output CSV file
df_jobs = pd.DataFrame(job_details)
df_jobs.to_csv(output_file, index=False, mode='a')
print(f"Scraping completed. Data saved to {output_file}.")
'''