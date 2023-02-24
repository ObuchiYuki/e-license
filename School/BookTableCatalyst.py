from selenium.webdriver.common.by import By

from Core.Error import CatalystError
from Core.Catalyst import Catalyst, CatalystLoader

from School.LoginCatalyst import LoginCatalyst
from School.DataType import *

class BookTableCatalyst(Catalyst):
    login_catalyst: LoginCatalyst

    def __init__(self, login_catalyst: LoginCatalyst, loader: CatalystLoader) -> None:
        super().__init__(loader)
        self.login_catalyst = login_catalyst

    def run(self):
        driver = self.driver
        self.login_catalyst.run()
        table = driver.find_element(By.CLASS_NAME, "yoyakuTable")
        date_titles = driver.find_elements(By.CSS_SELECTOR, "#ginou-scroll-day .date")
        date_list = table.find_elements(By.CLASS_NAME, "date")
        
        dates: list[Date] = []
        for date_element, date_title in zip(date_list, date_titles):
            frame_list = date_element.find_elements(By.TAG_NAME, "td")
            date_name = date_title.text.replace("\n", "").strip()

            date = Date(date_name, [])
            for i, frame_element in enumerate(frame_list):
                status = frame_element.get_attribute("class")
                frame = Frame(date_name, i + 8, FrameStatus.from_str(status))
                date.frames.append(frame)
            dates.append(date)
        
        return BookTable(dates)