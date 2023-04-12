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
from data_to_import import user_data, article, modified_article, deleted_article


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
        self.browser.quit()

    # 1 Regisztráció helyes adatokkal----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_registration(self):

        # Megkeresem a regisztráció gombot és rákattintok

        signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        signup_button.click()
        time.sleep(2)

        # Megkeresem a beviteli mezőket és elkdülöm az importált data fájlból a megfelelő adatokat kitöltésre

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

        # Ellenőrzöm, hogy megjelenik-e az ablak és benne a szöveg, hogy sikeres volt a bejelentkezés

        registration_confirmed = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))
        time.sleep(1)

        assert registration_confirmed.text == "Welcome!"

        ok_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        ok_button.click()

    # 2 Bejelentkezés helyes adatokkal----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_login(self):

        # Megkeresem a bejelentkezés gombot, rákattintok, majd megkeresem a beviteli mezőket, és a megfelelő importált adatokkal kitöltöm őket.

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
        time.sleep(2)

        # A bejelentkezett felületen kikeresem a profilomat jelző webelementet, és összehasonlítom, hogy megegyezik-e az email címhez tartozó felhasználónévvel.

        profile = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[2]

        time.sleep(2)
        assert profile.is_displayed
        assert profile.text == user_data['username']

    # 3 Adatkezelési nyilatkozat használata (cookies elfogadása)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

    # 4 Adatok listázása - tag-ek listázása ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_list_data(self):
        login(self.browser)

        # Elmentem a Popular tags résznél található tagek webelementjeit egy listába.

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        # Létrehozok egy új listát, majd végigiterálok a tagek webelementjein, és mindegyik text-jét elmentem az új listába, így visszakapom az összes taget szöveges formában.

        tag_list = []
        for tag in popular_tags:
            tag_list.append(tag.text)
        print(tag_list)

        # Ellenőrzöm hogy az így kapott lista hossza nem 0, tehát nem üres a lista.

        assert len(tag_list) != 0

    # 5 Több oldalas lista bejárása (lapozás) ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_all_pages(self):

        login(self.browser)

        # Megkeresem a lapozó gombok webelementjeit, és for ciklus segítségével végiterálok rajta

        page_links = self.browser.find_elements(By.CSS_SELECTOR, 'a[class ="page-link"]')

        # Felveszek egy oldal számlálót, amit minden iterációban növelek egyel, és összehasonlítom, hogy a száma megegyezik-e az aktuális lapozó gombon található oldalszámmal

        page_counter = 1
        for link in page_links:
            link.click()
            assert int(link.text) == page_counter
            page_counter += 1

        # Összehasonlítom hogy a lapozó gombok listájának hossza megegyezik-e a számlálóval (kivonok 1-et belőle, hiszen az utolsó iteráció végén is hozzáadott még egyet)

        assert len(page_links) == page_counter-1

    # 6 Új adat bevitel - új bejegyzés létrehozása ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_new_data(self):

        login(self.browser)

        # Kikeresem és rányomok az új bejegyzés létrehozása gombra

        new_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        new_article_btn.click()
        time.sleep(1)

        # Kikeresem az input mezőket és elküldöm az ipmortált data fájlból a megfelelő adatokat kitöltésre, majd rányomok a létrehozás gombra

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="ti-new-tag-input ti-valid"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        title_input.send_keys(article['title'])
        about_input.send_keys(article['about'])
        full_article_input.send_keys(article['full_article'])
        tags_input.send_keys(article['tags'])
        submit_button.click()

        # Helyes létrehozás esetén a bejegyzés oldalán vagyunk, ahol h1-es elemben jelenik meg a cím, ezt kikeresem, és ellenőrzöm, hogy megyezik-e a korábban megadottal

        h1_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        assert h1_title.text == article['title']

    # 7 Ismételt és sorozatos adatbevitel adatforrásból - több új bejegyzés létrehozása egyszerre----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_read_data(self):

        login(self.browser)

        # Megnyitom a csv fájlt olvasásra, az első sort kihagyom a beolvasásból

        with open('test/articles_to_read.csv', 'r', encoding='UTF-8') as file:
            articles = csv.reader(file, delimiter=',')
            next(articles)

            # Létrehozok egy listát a címeknek, a későbbi ellenőrzéshez
            title_list = []

            # For ciklus segítségével a fájl minden során végigiterálok, és minden iterációban kikeresem a megfelelő beviteli mezőket

            for row in articles:

                new_article(self.browser, row[0], row[1], row[2], row[3])

                # Elmentem a beolvasott sor első elemét (cím) a korábban létrehozott címlistába, későbbi ellenőrzéshez

                title_list.append(row[0])

            # Visszalépek a kezdőoldalra, és a korábban létrehozott címlista elemein végigmegyek,
            # és ellenőrzöm, hogy megegyező elnevezésű elem létezik-e az oldalon, tehát létrejött-e a bejegyzés.

            home_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
            home_btn.click()
            time.sleep(2)

            for title in title_list:
                assert (self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{title}')).is_displayed()

    # 8 Meglévő adat módosítás - bejegyzés szerkesztése ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_modify_data(self):

        # Bejelentkezek és létrehozok egy új bejegyzést

        login(self.browser)
        new_article(self.browser, article['title'], article['about'], article['full_article'], article['tags'])

        # Megkeresem a bejegyzés oldalán állva a szerkesztés gombot és rákattintok.

        edit_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="btn btn-sm btn-outline-secondary"]')))
        edit_btn.click()

        # Megkeresem a beviteli mezőket

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="ti-new-tag-input ti-valid"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        # Kitörlöm a beviteli mezőkből a korábbi adatokat, majd a beimportált data fájlból elkdülöm a módosított adatokat.

        title_input.clear()
        about_input.clear()
        full_article_input.clear()
        title_input.send_keys(modified_article['title'])
        about_input.send_keys(modified_article['about'])
        full_article_input.send_keys(modified_article['full_article'])
        tags_input.send_keys(modified_article['tags'])
        submit_button.click()
        time.sleep(1)

        # Visszanavigálok a főoldalra és ellenőrzöm, hogy találok-e olyan linket az oldalon,
        # amely szövege megegyezik a módosított bejegyzés címével, tehát megjelent-e a bejegyzés az oldalon.

        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()
        time.sleep(2)

        assert self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{modified_article["title"]}').is_displayed()

    # 9 Adat vagy adatok törlése - bejegyzés törlése ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_delete_data(self):

        # Bejelentkezek és létrehozok egy új bejegyzést

        login(self.browser)
        new_article(self.browser, deleted_article['title'], deleted_article['about'], deleted_article['full_article'], deleted_article['tags'])

        # Megkeresem a törlés gombot, és rákattintok

        delete_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-outline-danger btn-sm"]')))
        delete_btn.click()
        time.sleep(5)

        #Visszanavigálok a főoldalra és ellenőrzöm, hogy találok-e olyan linket az oldalon,
        # amely szövege megegyezik a létrehozott bejegyzés címével, ha nem, akkor törlődött a bejegyzés az oldalról.

        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()

        assert len(self.browser.find_elements(By.PARTIAL_LINK_TEXT, f'{deleted_article["title"]}')) == 0

    # 10 Adatok lementése felületről - tagek kiíratása csv fájlba ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_write_data(self):

        login(self.browser)

        # Elmentem a Popular tags résznél található tagek webelementjeit egy listába.

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        # Megnyitom a fájlt, és for ciklus segítségével végigiterálok a popular_tags elemein, és beleírom a fájlba a webelementek text-jeit.

        with open('test/tags_to_write', 'w', encoding="UTF-8") as tag_file:
            for tag in popular_tags:
                tag_file.write(tag.text)
                tag_file.write("\n")

        # Beolvasom a létrehozott fájlt, a tartalmát elmentem egy listába, majd megnézem, hogy a lista nem üres,
        # és a hossza megegyezik az eredeti popular_tags lista elemszámával

        tag_list_read = []
        with open('test/tags_to_write', 'r', encoding="UTF-8") as tag_file_read:
            tags = csv.reader(tag_file_read)
            for tag in tags:
                tag_list_read.append(tag)

        assert len(tag_list_read) > 0
        assert len(tag_list_read) == len(popular_tags)

    # 11 Kijelentkezés----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_logout(self):

        login(self.browser)

        # Kikeresem a kijelentkezés gombot, és rákattintok

        logout_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Log out')))
        logout_button.click()
        time.sleep(1)

        # Ellenőrzöm, hogy az oldalon látszik-e a bejelentkezés gomb, ha igen, akkor sikeresen kijelentkeztem

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        assert signin_button.is_displayed()
