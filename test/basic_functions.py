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


def screenshot(browser):
    allure.attach(browser.get_screenshot_as_png(),
                  name="test_login",
                  attachment_type=allure.attachment_type.PNG)

