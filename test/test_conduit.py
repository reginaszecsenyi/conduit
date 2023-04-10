import time
import csv
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from basic_functions import login, new_article
from data_to_import import user_data, article, modified_article


class TestConduit(object):

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)
        o.add_argument('--headless')
        o.add_argument('--no-sandbox')
        o.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=s, options=o)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        # time.sleep(1)
        self.browser.quit()

    # 1 Regisztráció ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_registration(self):
        signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        signup_button.click()
        time.sleep(2)

        username_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signup = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        username_input.send_keys(user_data['username'])
        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])
        confirm_signup.click()

        registration_confirmed = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))
        time.sleep(1)

        assert registration_confirmed.text == "Welcome!"

        ok_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        ok_button.click()

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

        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])
        confirm_signin.click()
        time.sleep(5)

        # A bejelentkezett felületen kikeresem a profilomat jelző webelementet, és összehasonlítom, hogy megegyezik-e az email címhez tartozó felhasználónévvel.

        profile = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')[2]))
        assert profile.is_displayed
        assert profile.text == user_data['username']

    # 3 Adatkezelési nyilatkozat használata----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_data_cookies(self):
        # Ellenőrzöm hogy megjelent-e az adatkezelési panel.

        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        assert cookie_policy_panel.is_displayed()

        # Kikeresem az elfogadási gomb webelementjét és megnyomom.

        accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        time.sleep(1)
        accept_cookies_btn.click()
        time.sleep(1)

        # Ellenőrzöm, hogy létezik-e még a korábbi adatkezelési panel, vagy már nem található az oldalon.

        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

    # 4 Adatok listázása ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_list_data(self):
        login(self.browser)

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        tag_list = []
        for tag in popular_tags:
            tag_list.append(tag.text)
        print(tag_list)

        assert len(tag_list) != 0

    # 5 Több oldalas lista bejárása----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_all_pages(self):

        login(self.browser)

        # Megkeresem a lapozó gombok webelementjeit, és végignyomom az összeset

        page_links = self.browser.find_elements(By.CSS_SELECTOR, 'a[class ="page-link"]')

        pages = []
        for link in page_links:
            link.click()
            pages.append(link)

        # A gombok végignyomása során minden megnyomott elemet egy listába raktam, és ellenőrzöm, hogy ennek a listának a hossza megegyezik-e a talált webelementek listájának hosszával.

        assert len(page_links) == len(pages)

    # 6 Új adat bevitel ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_new_data(self):

        login(self.browser)

        # Kikeresem és rányomok az új bejegyzés létrehozására

        new_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        time.sleep(1)
        new_article_btn.click()

        # Kikeresem az input mezőket és elküldöm a dictionary megfelelő elemeit kitöltésre, majd rányomok a létrehozás gombra

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[class="ti-new-tag-input-wrapper"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        title_input.send_keys(article['title'])
        about_input.send_keys(article['about'])
        full_article_input.send_keys(article['full_article'])
        # tags_input.send_keys(article['tags'])
        submit_button.click()

        # Helyes létrehozás esetén a bejegyzés oldalán vagyunk, ahol h1-es elemben jelenik meg a cím, ezt kikeresem, és ellenőrzöm, hogy megyezik-e a korábban megadottal

        h1_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        assert h1_title.text == article['title']

    # 7 Ismételt és sorozatos adatbevitel adatforrásból----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_read_data(self):

        login(self.browser)

        # Megnyitom a csv fájlt olvasásra

        with open('test/articles_to_read.csv', 'r', encoding='UTF-8') as file:
            articles = csv.reader(file, delimiter=',')
            next(articles)

            # Létrehozok egy listát a címeknek, későbbi ellenőrzéshez
            title_list = []

            # Ciklus segítségével a csv fájl minden sorához kikeresem a megfelelő mezőket.
            for row in articles:
                new_article_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
                time.sleep(1)
                new_article_btn.click()

                title_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
                about_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
                full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
                tags_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'li[class="ti-new-tag-input-wrapper"]')))
                submit_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

                # Elmentem a beolvasott sorok első elemét (cím) egy korábban létrehozott listába, későbbi ellenőrzéshez.
                title_list.append(row[0])

                # Elküldöm a kikeresett mezőkbe a megfelelő adatokat.

                title_input.send_keys(row[0])
                about_input.send_keys(row[1])
                full_article_input.send_keys(row[2])
                # tags_input.send_keys(row[3])
                submit_button.click()

            # Visszalépek a kezdőoldalra, és a korábban létrehozott címlista elemein végigmegyek, és ellenőrzöm, hogy megegyező elnevezésű elem létezik-e az oldalon, tehát létrejött-e a cikk.

            home_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
            home_btn.click()

            time.sleep(2)

            for title in title_list:
                assert (self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{title}')).is_displayed()

    # 8 Meglévő adat módosítás ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_modify_data(self):

        login(self.browser)

        new_article(self.browser)

        # article_url = article["title"].replace(' ', '-')
        # self.browser.get(f'http://localhost:1667/#/articles/{article_url.lower()}')

        edit_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="btn btn-sm btn-outline-secondary"]')))
        edit_btn.click()

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[class="ti-new-tag-input-wrapper"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        title_input.clear()
        about_input.clear()
        full_article_input.clear()
        title_input.send_keys(modified_article['title'])
        about_input.send_keys(modified_article['about'])
        full_article_input.send_keys(modified_article['full_article'])
        submit_button.click()
        time.sleep(1)

        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()
        time.sleep(2)

        assert self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{modified_article["title"]}').is_displayed()

    # 9 Adat vagy adatok törlése ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_delete_data(self):

        login(self.browser)

        new_article(self.browser)
        delete_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-outline-danger btn-sm"]')))
        delete_btn.click()
        time.sleep(5)

        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()

        assert not self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{article["title"]}').is_displayed()

    # 10 Adatok lementése felületről ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_write_data(self):

        login(self.browser)

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        tag_list = []
        for tag in popular_tags:
            tag_list.append(tag.text)
        print(tag_list)

        with open('test/tags_to_write', 'w', encoding="UTF-8") as tag_file:
            tag_file.write(str(tag_list))

    # 11 Kijelentkezés----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_logout(self):

        login(self.browser)

        # Kikeresem a kijelentkezés gombot

        logout_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Log out')))
        logout_button.click()
        time.sleep(1)

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        assert signin_button.is_displayed()
