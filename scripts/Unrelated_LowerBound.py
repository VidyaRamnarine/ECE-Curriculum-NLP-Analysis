import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager


option = webdriver.ChromeOptions()
option.add_argument('--log-level=1')


# URL of the course page
url = "https://www.manchester.ac.uk/study/undergraduate/courses/2025/00653/bsc-psychology/course-details/PSYC10711#course-unit-details"


def scrape_course_details_with_selenium(url):
    #Intialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

    try:
        # Open the webpage
        driver.get(url)
        
        # Wait for the course content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "course-profile-content"))
        )
        
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract course title
        course_title = soup.find("h2", id="course-unit-details").text.strip()

        # Extract course code from the fact file table
        fact_file_table = soup.find("table", class_="course-unit-fact-file")
        course_code = None
        for row in fact_file_table.find_all("tr"):
            key = row.find("th").text.strip()
            if key == "Unit code":
                course_code = row.find("td").text.strip()
                break

        # Extract and combine everything from Overview to Study Hours into a single description string
        sections = [
            "Overview",
            "Aims",
            "Teaching and learning methods",
            "Knowledge and understanding",
            "Intellectual skills",
            "Practical skills",
            "Transferable skills and personal qualities",
            "Assessment methods",
            "Recommended reading",
            "Study hours",
        ]
        description_parts = []
        for section in sections:
            header = soup.find("h3", text=section)
            if header:
                content = header.find_next("div", class_="text") or header.find_next("table")
                if content:
                    description_parts.append(f"{section}: {content.text.strip()}")

        # Combine all parts into a single description
        description = " ".join(description_parts).replace("\n", " ").strip()

        # Return the extracted details
        return {
            "Course Title": course_title,
            "Course Code": course_code,
            "Description": description,
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the WebDriver
        driver.quit()

# Scrape the course details
course_data = scrape_course_details_with_selenium(url)

# Save the data to a CSV file
if course_data:
    output_file = "course_details.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Course Title", "Course Code", "Description"])
        # Write the course details row
        writer.writerow([course_data["Course Title"], course_data["Course Code"], course_data["Description"]])

    print(f"Course details saved to {output_file}")
