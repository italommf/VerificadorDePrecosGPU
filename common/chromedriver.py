from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

class UndetectedChromeDriver:

    def __init__(self, headless=False):
        self.headless = headless
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-sync")
            options.add_argument("--metrics-recording-only")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-translate")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--mute-audio")

            self._driver = uc.Chrome(options=options)
        return self._driver

    def quit(self):
        if self._driver:
            self._driver.quit()
            self._driver = None


class ChromeDriver:

    def __init__(self, headless=False):
        self.headless = headless
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            options = Options()
            if self.headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self._driver = webdriver.Chrome(options=options)
        return self._driver

    def quit(self):
        if self._driver:
            self._driver.quit()
            self._driver = None