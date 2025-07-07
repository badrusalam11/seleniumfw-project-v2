import time
from seleniumfw.runner import Runner
from seleniumfw.browser_factory import BrowserFactory

def run():
    browser_factory = BrowserFactory()
    driver = browser_factory.create_driver()
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    driver.maximize_window()
    time.sleep(3)
    driver.save_screenshot("cura-demo.png")