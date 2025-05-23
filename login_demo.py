from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from webdriver_manager.chrome import ChromeDriverManager as CDM
import logging

url = "https://www.saucedemo.com/"
name_insert = "standard_user"
pass_insert = "secret_sauce"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Browser_set:
    def __init__(self):
        self.driver = None
    
    def start_browser(self):
        self.driver = webdriver.Chrome(service=Service(CDM().install()))
        self.driver.get(url)

    def quit_browser(self):
        if self.driver:
            self.driver.quit()


class LoginFlow:
    def __init__(self, driver):
        self.driver = driver

    def username_input(self):
        username = self.driver.find_element(By.ID, "user-name")
        username.send_keys(name_insert)

    def pass_input(self):
        password = self.driver.find_element(By.ID, "password")
        password.send_keys(pass_insert)

    def loginbutton_click(self):
        loginbutton = self.driver.find_element(By.ID, "login-button")
        loginbutton.click()

    def run_login(self):
        try:
            WDW (self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "login-box"))
            )
            self.username_input()
            self.pass_input()
            self.loginbutton_click()
            input("手動")
            self.login_judge()
        except Exception as e:
            print("login-boxの要素が見つかりませんでした", e) 

    def login_judge(self):
        try:
            WDW(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
            )
            logging.info("ログイン成功")
            self.driver.save_screenshot("login_successed.png")
        except Exception as e:
            logging.error("ログイン失敗")
            self.driver.save_screenshot("login_failed.png")
            raise AssertionError("ログイン失敗") from e

browser = Browser_set()
browser.start_browser()
login = LoginFlow(browser.driver)
login.run_login()
input("終了前")
browser.quit_browser()