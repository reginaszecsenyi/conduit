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
        # o.add_argument('--headless')
        # o.add_argument('--no-sandbox')
        # o.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=s, options=o)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        time.sleep(1)
        self.browser.quit()

    # 1 Regisztráció ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_registration(self):
    #     signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
    #     signup_button.click()
    #     time.sleep(2)
    #
    #     username_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
    #     email_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
    #     password_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
    #     confirm_signup = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
    #
    #     username_input.send_keys('tesztfelhasznalo10')
    #     email_input.send_keys('teszt9@teszt.com')
    #     password_input.send_keys('Teszt456')
    #     confirm_signup.click()
    #
    #
    #     registration_confirmed = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))
    #
    #     assert registration_confirmed.text == "Welcome!"
    #
    #     ok_button = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
    #     ok_button.click()

    # 2 Bejelentkezés ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_login(self):
        # Rákattintok a főoldalon a Sign up gombra, majd kikeresem a beviteli mezők webelementjeit, és a megfelelő adatokkal kitöltöm a mezőket.

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        signin_button.click()

        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signin = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        confirm_signin.click()
        time.sleep(1)

        # A bejelentkezett felületen kikeresem a profilomat jelző webelementet, és összehasonlítom, hogy megegyezik-e az email címhez tartozó felhasználónévvel.

        # nav_links = WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        # time.sleep(1)
        # profile = nav_links[2]
        # assert profile.text == self.username

    # 3 Adatkezelési nyilatkozat használata----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_data_cookies(self):
        pass
        # Ellenőrzöm hogy megjelent-e az adatkezelési panel.

        # cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        # assert cookie_policy_panel.is_displayed()
        #
        # # Kikeresem az elfogadási gomb webelementjét és megnyomom.
        #
        # accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        # time.sleep(1)
        # accept_cookies_btn.click()
        # time.sleep(1)
        #
        # # Ellenőrzöm, hogy létezik-e még a korábbi adatkezelési panel, vagy már nem található az oldalon.
        #
        # assert len(self.browser.find_elements(By.ID, 'cookie-polidy-panel')) == 0

    # 4 Adatok listázása ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_list_data(self):
    #     pass

    # 5 Több oldalas lista bejárása----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_all_pages(self):
        pass
        # Bejelentkezés

        # signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        # signin_button.click()
        #
        # email_input = WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        # password_input = WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        # confirm_signin = WebDriverWait(self.browser, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
        #
        # email_input.send_keys(self.email)
        # password_input.send_keys(self.password)
        # confirm_signin.click()
        # time.sleep(1)
        #
        # accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        # accept_cookies_btn.click()
        #
        # # Megkeresem a lapozó gombok webelementjeit, és végignyomom az összeset
        #
        # page_links = self.browser.find_elements(By.CSS_SELECTOR, 'a[class ="page-link"]')
        #
        # pages = []
        # for link in page_links:
        #     link.click()
        #     pages.append(link)

        # A gombok végignyomása során minden megnyomott elemet egy listába raktam, és ellenőrzöm, hogy ennek a listának a hossza megegyezik-e a talált webelementek listájának hosszával.

        # assert len(page_links) == len(pages)

        # next_button = page_links[0]
        # while next_button.get_attribute('class') != 'page-item':
        #     next_button.click()

    # 6 Új adat bevitel ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_new_data(self):
    #     # Bejelentkezés
    #
    #     signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
    #     signin_button.click()
    #
    #     email_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
    #     password_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
    #     confirm_signin = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
    #
    #     email_input.send_keys(self.email)
    #     password_input.send_keys(self.password)
    #     confirm_signin.click()
    #     time.sleep(1)
    #
    #     accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
    #     accept_cookies_btn.click()
    #
    #     # Új bejegyzés létrehozása
    #
    #     # Kikeresem és rányomok az új bejegyzés létrehozására
    #
    #     new_article_btn = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/editor"]')
    #     new_article_btn.click()
    #
    #     # Elmentem egy dictionaryba a beírandó adatokat, hogy könnyebb legyen hivatkozni rájuk
    #
    #     article = {
    #         "title": "The Title",
    #         "about": "What the article is about?",
    #         "full_article": "Write the full article here",
    #         "tags": "article, tag"
    #     }
    #
    #     # Kikeresem az input mezőket és elküldöm a dictionary megfelelő elemeit kitöltésre, majd rányomok a létrehozás gombra
    #
    #     title_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
    #     about_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
    #     full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
    #     tags_input = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="vue-tags-input form-control"]')))
    #     submit_button = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    #
    #     title_input.send_keys(article['title'])
    #     about_input.send_keys(article['about'])
    #     full_article_input.send_keys(article['full_article'])
    #     # tags_input.send_keys(article['tags'])          #tag bevitele nem sikerül
    #     submit_button.click()
    #
    #     # Helyes létrehozás esetén a bejegyzés oldalán vagyunk, ahol h1-es elemben jelenik meg a cím, ezt kikeresem, és ellenőrzöm, hogy megyezik-e a korábban megadottal
    #
    #     h1_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    #     assert h1_title.text == article['title']

    # 7 Ismételt és sorozatos adatbevitel adatforrásból----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_read_data(self):
    #     pass
    #
    # 8 Meglévő adat módosítás ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_modify_data(self):
    #     pass
    #
    # 9 Adat vagy adatok törlése ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_delete_data(self):
    #     pass
    #
    # 10 Adatok lementése felületről ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_write_data(self):
    #     pass
    #
    # 11 Kijelentkezés----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # def test_logout(self):
    #     logout_button = self.browser.find_element(By.CSS_SELECTOR, 'a[active-class="active"]')
    #     logout_button.click()
    #
    #     nav_links = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
    #     time.sleep(1)
    #     profile = nav_links[2]
    #     assert profile.text == self.username
