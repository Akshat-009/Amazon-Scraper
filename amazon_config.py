from selenium import webdriver

DIRECTORY='reports'
NAME="ps4"
BASE_URL="https://www.amazon.in/"
CURRENCY="₹"
def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver",chrome_options=options)
def get_web_driver_options():
    return webdriver.ChromeOptions()
def set_ignore_certificate_error(options):
    options.add_argument("--ignore-certificate-errors")
def set_browser_as_incognito(options):
    options.add_argument("--incognito")