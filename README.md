Indeed Job Scraper
Overview
This project is a Python-based web scraper designed to extract job listings from Indeed.com using two methods: Selenium for dynamic JavaScript-heavy pages and BeautifulSoup with requests for static content. It scrapes job details such as title, company, location, salary, summary, and URL, and saves the results to CSV and JSON files.
Features

Selenium-based scraping: Handles JavaScript-rendered pages for reliable data extraction.
Requests-based scraping: A lightweight fallback method for static content (less reliable due to JavaScript dependencies).
CAPTCHA detection: Checks for CAPTCHA challenges during scraping.
Human-like delays: Implements random delays to mimic human behavior and avoid detection.
Data storage: Saves scraped job data to both CSV and JSON formats.
Error handling: Robust logging and exception handling to ensure stability.
Configurable search: Allows customization of job title, location, and number of pages to scrape.

Prerequisites

Python 3.8+
Dependencies:
beautifulsoup4: For parsing HTML content.
selenium: For handling dynamic web pages.
requests: For making HTTP requests.
webdriver-manager: For managing WebDriver binaries (e.g., ChromeDriver).


WebDriver: A compatible browser driver (e.g., ChromeDriver) is required for Selenium. The webdriver-manager package can automatically handle this.
Internet connection: Required to access Indeed.com and fetch job listings.

Installation

Clone the repository:git clone <repository-url>
cd <repository-directory>


Install dependencies:pip install -r requirements.txt


Ensure a compatible browser (e.g., Chrome) is installed for Selenium.

Usage

Configure the scraper by updating the constants.py file with the desired BASE_URL (e.g., https://www.indeed.com).
Run the script:python indeed_scraper.py


The script will:
Search for jobs based on the specified job_title (e.g., "Python Developer") and location (e.g., "Delhi").
Scrape the specified number of pages (num_pages).
Save results to indeed_jobs.csv and indeed_jobs.json (or backup files if the Selenium method fails).


Example output:Starting Indeed job scraping...
Searching for: Python Developer in Delhi
Pages to scrape: 3
Found 45 jobs!
First 3 jobs found:
1. Python Developer
   Company: ABC Corp
   Location: Delhi
   Salary: ₹50,000 a month
   Summary: Develop and maintain Python-based applications...
   URL: https://www.indeed.com/viewjob?jk=...
...



File Structure

indeed_scraper.py: Main script containing the IndeedScraper class and scraping logic.
init.py: Contains the ScraperInitializer base class for setting up Selenium and requests sessions.
utils.py: Utility functions for human-like delays, CAPTCHA detection, and saving data to CSV/JSON.
constants.py: Configuration file for the base URL and other constants.
requirements.txt: List of required Python packages.

Customization

Job Search Parameters: Modify job_title, location, and num_pages in the if __name__ == "__main__": block of indeed_scraper.py.
Output Files: Change the output filenames in the save_to_csv and save_to_json calls.
Logging: Adjust logging settings in init.py for more or less verbose output.

Notes

CAPTCHA Handling: The scraper detects CAPTCHAs but does not solve them. Manual intervention or a CAPTCHA-solving service is required if detected.
Selenium vs. Requests: Selenium is more reliable for Indeed due to its JavaScript-heavy pages, but the requests method is included as a lightweight backup.
Rate Limiting: The scraper includes random delays to avoid being blocked, but excessive scraping may still trigger rate limits or CAPTCHAs.
Data Accuracy: Some fields (e.g., salary) may not always be available and will be marked as 'N/A'.

Limitations

The requests-based method may fail to extract data from pages that rely heavily on JavaScript.
CAPTCHA challenges can interrupt scraping, requiring manual intervention.
The scraper is tailored for Indeed.com and may need adjustments for other job boards.

License
This project is licensed under the MIT License. See the LICENSE file for details.
