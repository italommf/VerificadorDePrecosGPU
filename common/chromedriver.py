import undetected_chromedriver as uc

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
            self._driver = uc.Chrome(options=options)
        return self._driver

    def quit(self):
        if self._driver:
            self._driver.quit()
            self._driver = None