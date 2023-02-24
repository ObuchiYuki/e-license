from dataclasses import dataclass
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import chromedriver_binary # required
import undetected_chromedriver as uc

from Core.Logger import Logger

def selenium_make(window_size: tuple[int, int] = (1201, 1001)) -> WebDriver: 
    options = webdriver.ChromeOptions()
    
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
    options.add_argument("--user-data-dir=/Users/yuki/Developer/ChromeData")
    
    driver = uc.Chrome(options=options, headless=True)
    driver.set_window_size(window_size[0], window_size[1])
    
    return driver

@dataclass
class CatalystLoader:
    driver: WebDriver
    logger: Logger

class Catalyst:
    driver: WebDriver
    logger: Logger

    def __init__(self, loader: CatalystLoader):
        self.driver = loader.driver
        self.logger = loader.logger
    
    def sleep(self, duration: float):
        sleep(duration)

    