
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


class TestConduit(object):
    username = 'tesztfelhasznalo10'
    email = 'klviaypoieqopuijxg@tcwlm.com'
    password = 'Teszt456'

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)

        self.browser = webdriver.Chrome(service=s, options=o)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        time.sleep(1)
        #self.browser.quit()

    def test_registration(self):

        signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        signup_button.click()
        time.sleep(2)

        username_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signup = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        username_input.send_keys('tesztfelhasznalo10')
        email_input.send_keys('teszt6@teszt.com')
        password_input.send_keys('Teszt456')
        confirm_signup.click()

        #Nem fut le az assert
        registration_confirmed = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-text"]')))
        time.sleep(2)
        assert registration_confirmed.get_attribute('style') == 'Your registration was successful!'

        ok_button = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        ok_button.click()


    def test_login(self):

        #Rákattintok a főoldalon a Sign up gombra, majd kikeresem a beviteli mezők webelementjeit, és a megfelelő adatokkal kitöltöm a mezőket.

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        signin_button.click()

        email_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signin = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        confirm_signin.click()
        time.sleep(1)

        #A bejelentkezett felületen kikeresem a profilomat jelző webelementet, és összehasonlítom, hogy megegyezik-e az email címhez tartozó felhasználónévvel.

        nav_links = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        time.sleep(1)
        profile = nav_links[2]
        assert profile.text == self.username

    def test_data_cookies(self):

        #Ellenőrzöm hogy megjelent-e az adatkezelési panel.

        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        assert cookie_policy_panel.is_displayed()

        #Kikeresem az elfogadási gomb webelementjét és megnyomom.

        accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        time.sleep(1)
        accept_cookies_btn.click()
        time.sleep(1)

        #Ellenőrzöm, hogy létezik-e még a korábbi adatkezelési panel, vagy már nem található az oldalon.

        assert len(self.browser.find_elements(By.ID, 'cookie-polidy-panel')) == 0

    # def test_list_data(self):
    #     pass
    #
    # def test_all_pages(self):
    #     pass
    #
    # def test_new_data(self):
    #     pass
    #
    # def test_read_data(self):
    #     pass
    #
    # def test_modify_data(self):
    #     pass
    #
    # def test_delete_data(self):
    #     pass
    #
    # def test_write_data(self):
    #     pass
    #
    # def test_logout(self):
    #     pass



