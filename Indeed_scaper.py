from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urljoin
from init import ScraperInitializer
from utils import human_delay, check_for_captcha, save_to_csv, save_to_json
from constants import BASE_URL
import requests


class IndeedScraper(ScraperInitializer):
    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL

    def search_jobs_selenium(self, job_title, location, num_pages=1):
        """Search jobs using Selenium for JavaScript-heavy pages"""
        driver = None
        jobs_data = []
        try:
            driver = self.setup_selenium_driver()
            driver.get(self.base_url)
            human_delay(2, 4)

            if check_for_captcha(driver):
                self.logger.error("CAPTCHA detected. Please solve it manually or use a CAPTCHA-solving service.")
                return jobs_data

            job_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "text-input-what"))
            )
            location_input = driver.find_element(By.ID, "text-input-where")
            job_input.clear()
            job_input.send_keys(job_title)
            human_delay(1, 2)
            location_input.clear()
            location_input.send_keys(location)
            human_delay(1, 2)

            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            human_delay(3, 6)

            if check_for_captcha(driver):
                self.logger.error("CAPTCHA detected after search. Please solve it manually.")
                return jobs_data

            for page in range(num_pages):
                self.logger.info(f"Scraping page {page + 1}")
                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
                    )
                    jobs = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
                    for job in jobs:
                        try:
                            job_data = self.extract_job_data_selenium(job, driver)
                            if job_data:
                                jobs_data.append(job_data)
                        except Exception as e:
                            self.logger.error(f"Error extracting job data: {e}")
                            continue

                    if page < num_pages - 1:
                        try:
                            next_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next Page']"))
                            )
                            driver.execute_script("arguments[0].click();", next_button)
                            human_delay(4, 8)
                            if check_for_captcha(driver):
                                self.logger.error("CAPTCHA detected on page navigation.")
                                break
                        except TimeoutException:
                            self.logger.info("No more pages available")
                            break
                except TimeoutException:
                    self.logger.error(f"Timeout waiting for job listings on page {page + 1}")
                    break

        except Exception as e:
            self.logger.error(f"Error during Selenium scraping: {e}")
        finally:
            if driver:
                driver.quit()
        return jobs_data

    def extract_job_data_selenium(self, job_element, driver):
        """Extract job data from a job element using Selenium"""
        try:
            job_data = {}
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "h2.jobTitle a span")
                job_data['title'] = title_element.text.strip()
            except NoSuchElementException:
                job_data['title'] = 'N/A'

            try:
                company_element = job_element.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
                job_data['company'] = company_element.text.strip()
            except NoSuchElementException:
                job_data['company'] = 'N/A'

            try:
                location_element = job_element.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']")
                job_data['location'] = location_element.text.strip()
            except NoSuchElementException:
                job_data['location'] = 'N/A'

            try:
                salary_element = job_element.find_element(By.CSS_SELECTOR, "div[data-testid='attribute_snippet_testid']")
                job_data['salary'] = salary_element.text.strip()
            except NoSuchElementException:
                job_data['salary'] = 'N/A'

            try:
                summary_element = job_element.find_element(By.CSS_SELECTOR, "div.job-snippet")
                job_data['summary'] = summary_element.text.strip()
            except NoSuchElementException:
                job_data['summary'] = 'N/A'

            try:
                link_element = job_element.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                job_data['url'] = link_element.get_attribute('href')
            except NoSuchElementException:
                job_data['url'] = 'N/A'

            return job_data
        except Exception as e:
            self.logger.error(f"Error extracting job data: {e}")
            return None

    def search_jobs_requests(self, job_title, location, num_pages=1):
        """Search jobs using requests (less reliable due to JavaScript)"""
        jobs_data = []
        for page in range(num_pages):
            try:
                url = f"{self.base_url}/jobs"
                params = {
                    'q': job_title,
                    'l': location,
                    'start': page * 10
                }
                headers = self.get_random_headers()
                headers['DNT'] = '1'  # Do Not Track for additional realism
                response = self.session.get(url, params=params, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                if "verify you are not a bot" in response.text.lower():
                    self.logger.error("CAPTCHA detected in requests method")
                    return jobs_data
                jobs = soup.find_all('div', {'data-jk': True})
                for job in jobs:
                    job_data = self.extract_job_data_requests(job)
                    if job_data:
                        jobs_data.append(job_data)
                human_delay(5, 12)
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"HTTP error scraping page {page + 1}: {e}")
                continue
            except Exception as e:
                self.logger.error(f"Error scraping page {page + 1}: {e}")
                continue
        return jobs_data

    def extract_job_data_requests(self, job_soup):
        """Extract job data from BeautifulSoup element"""
        try:
            job_data = {}
            title_elem = job_soup.find('span', {'title': True})
            job_data['title'] = title_elem.get('title', 'N/A') if title_elem else 'N/A'

            company_elem = job_soup.find('span', {'data-testid': 'company-name'})
            job_data['company'] = company_elem.text.strip() if company_elem else 'N/A'

            location_elem = job_soup.find('div', {'data-testid': 'text-location'})
            job_data['location'] = location_elem.text.strip() if location_elem else 'N/A'

            salary_elem = job_soup.find('div', {'data-testid': 'attribute_snippet_testid'})
            job_data['salary'] = salary_elem.text.strip() if salary_elem else 'N/A'

            summary_elem = job_soup.find('div', class_='job-snippet')
            job_data['summary'] = summary_elem.text.strip() if summary_elem else 'N/A'

            link_elem = job_soup.find('a', href=True)
            job_data['url'] = urljoin(self.base_url, link_elem['href']) if link_elem and link_elem['href'] else 'N/A'

            return job_data
        except Exception as e:
            self.logger.error(f"Error extracting job data: {e}")
            return None

if __name__ == "__main__":
    scraper = IndeedScraper()
    job_title = "Python Developer"
    location = "Delhi"
    
    num_pages = 3

    print("Starting Indeed job scraping...")
    print(f"Searching for: {job_title} in {location}")
    print(f"Pages to scrape: {num_pages}")

    try:
        jobs = scraper.search_jobs_selenium(job_title, location, num_pages)
    except Exception as e:
        print(f"Selenium scraping failed: {e}")
        jobs = []

    if jobs:
        print(f"\nFound {len(jobs)} jobs!")
        save_to_csv(jobs, 'indeed_jobs.csv', scraper.logger)
        save_to_json(jobs, 'indeed_jobs.json', scraper.logger)

        print("\nFirst 3 jobs found:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
            print(f"   Salary: {job.get('salary', 'N/A')}")
            summary = job.get('summary', 'N/A')
            if summary != 'N/A':
                summary = summary[:150] + "..." if len(summary) > 150 else summary
                print(f"   Summary: {summary}")
            print(f"   URL: {job.get('url', 'N/A')}")
    else:
        print("No jobs found with Selenium! Trying requests method as backup...")
        jobs = scraper.search_jobs_requests(job_title, location, num_pages)
        if jobs:
            print(f"Found {len(jobs)} jobs with requests method!")
            save_to_csv(jobs, 'indeed_jobs_backup.csv', scraper.logger)
            save_to_json(jobs, 'indeed_jobs_backup.json', scraper.logger)
        else:
            print("No jobs found with requests method either!")