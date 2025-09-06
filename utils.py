import random
import time
import csv
import json
import logging
from selenium.webdriver.common.by import By

def human_delay(min_seconds=2, max_seconds=8):
    """Add human-like delays between requests"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def check_for_captcha(driver):
    """Check if a CAPTCHA is present on the page"""
    try:
        captcha = driver.find_elements(By.XPATH, "//*[contains(text(), 'CAPTCHA') or contains(text(), 'verify you are not a bot')]")
        return len(captcha) > 0
    except:
        return False

def save_to_csv(jobs_data, filename='indeed_jobs.csv', logger=None):
    """Save job data to CSV file"""
    if not jobs_data:
        if logger:
            logger.warning("No job data to save to CSV")
        return
    fieldnames = ['title', 'company', 'location', 'salary', 'summary', 'url']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs_data:
            writer.writerow(job)
    if logger:
        logger.info(f"Saved {len(jobs_data)} jobs to {filename}")

def save_to_json(jobs_data, filename='indeed_jobs.json', logger=None):
    """Save job data to JSON file"""
    if not jobs_data:
        if logger:
            logger.warning("No job data to save to JSON")
        return
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(jobs_data, jsonfile, indent=2, ensure_ascii=False)
    if logger:
        logger.info(f"Saved {len(jobs_data)} jobs to {filename}")