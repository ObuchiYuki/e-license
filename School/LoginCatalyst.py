from selenium.webdriver.common.by import By

from Core.Error import CatalystError
from Core.Catalyst import Catalyst, CatalystLoader

from School.CommandConfiguration import CommandConfiguration

class LoginCatalyst(Catalyst):
    config: CommandConfiguration

    def __init__(self, config: CommandConfiguration, loader: CatalystLoader) -> None:
        super().__init__(loader)
        self.config = config

    def run(self):
        driver = self.driver
        driver.get(self.config.loginurl)
    
        self.sleep(0.1)

        student_id_field = driver.find_element(By.ID, "studentId")
        password_id_field = driver.find_element(By.ID, "password")

        student_id_field.send_keys(self.config.username)
        password_id_field.send_keys(self.config.password)

        submit_button = driver.find_element(By.ID, "login")
        submit_button.click()

        self.sleep(0.1)

        tables = driver.find_elements(By.CLASS_NAME, "yoyakuTable")
        if len(tables) == 0:
            raise CatalystError("Login failed.")
