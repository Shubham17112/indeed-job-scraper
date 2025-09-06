import requests
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constants import USER_AGENTS, BASE_HEADERS

class ScraperInitializer:
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = USER_AGENTS
        self.base_headers = BASE_HEADERS
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def get_random_headers(self):
        """Generate headers with random User-Agent and optional Referer"""
        headers = self.base_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        if random.random() > 0.7:
            headers['Referer'] = 'https://www.google.com/'
        return headers

    def setup_selenium_driver(self, headless=True):
        """Setup Selenium WebDriver with advanced evasion techniques"""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            user_agent = random.choice(self.user_agents)
            chrome_options.add_argument(f'--user-agent={user_agent}')
            window_sizes = ['1920,1080', '1366,768', '1440,900', '1536,864']
            chrome_options.add_argument(f'--window-size={random.choice(window_sizes)}')
            chrome_options.add_argument('--disable-gpu')  # Disable GPU to avoid AMD errors
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to initialize Selenium WebDriver: {e}")
            raise