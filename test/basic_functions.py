import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from data_to_import import user_data, article

def login(browser):
    signin_button = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href = "#/login"]')))
    signin_button.click()

    email_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
    password_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
    confirm_signin = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

    email_input.send_keys(user_data['email'])
    password_input.send_keys(user_data['password'])
    confirm_signin.click()
    time.sleep(2)

def new_article(browser, title, about, full_article, tags):
    new_article_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
    time.sleep(1)
    new_article_btn.click()

    title_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
    about_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
    full_article_input = WebDriverWait(browser, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
    tags_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="ti-new-tag-input ti-valid"]')))
    submit_button = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))


    title_input.send_keys(title)
    about_input.send_keys(about)
    full_article_input.send_keys(full_article)
    tags_input.send_keys(tags)
    submit_button.click()

def screenshot(browser):
    allure.attach(browser.get_screenshot_as_png(),
                  name="test_login",
                  attachment_type=allure.attachment_type.PNG)

