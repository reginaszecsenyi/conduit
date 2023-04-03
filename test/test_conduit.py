
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# username = 'tesztfelhasznalo20'
# email = 'klviaypoieqopuijxg@tcwlm.com'
# password = 'Teszt456'

class TestConduit(object):

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)

        self.browser = webdriver.Chrome(service=s, options=o)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        #self.browser.quit()

    def test_registration(self):

        signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        signup_button.click()
        time.sleep(2)

        username_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signup = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        username_input.send_keys('tesztfelhasznalo20')
        email_input.send_keys('klviaypoieqopuijxg@tcwlm.com')
        password_input.send_keys('Teszt456')
        confirm_signup.click()


    def test_login(self):
        pass
        # signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        # signin_button.click()
        # time.sleep(2)
        #
        # username_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        # password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        #
        # username_input.send_keys('tesztfelhasznalo20')
        # password_input.send_keys('Teszt456')


    def test_data_cookies(self):
        pass

        # accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        # accept_cookies_btn.click()


    def test_list_data(self):
        pass

    def test_all_pages(self):
        pass

    def test_new_data(self):
        pass

    def test_read_data(self):
        pass

    def test_modify_data(self):
        pass

    def test_delete_data(self):
        pass

    def test_write_data(self):
        pass

    def test_logout(self):
        pass



