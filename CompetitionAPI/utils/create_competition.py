from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from forms import *
import logging

WAIT_TIMEOUT = 10


# I hate typing this out so let's shrink "get_web_element_from_xpath"
def gwefxp(driver: WebDriver, xpath: str) -> WebElement:
    return driver.find_element(By.XPATH, xpath)


# "wait_until_visible_element_xpath"
def wuvexp(driver: WebDriver, xpath: str) -> None:
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


def login(driver: WebDriver):
    wuvexp(driver, '//*[@id="loginiframe"]')

    iframe = gwefxp(driver, '//*[@id="loginiframe"]')
    driver.switch_to.frame(iframe)

    wuvexp(driver, '//*[@id="AuthEmail"]')
    email_login = gwefxp(driver, '//*[@id="AuthEmail"]')
    email_login.send_keys("nixotica@gmail.com")

    pass_login = gwefxp(driver, '//*[@id="AuthPassword"]')
    pass_login.send_keys("Quoridor24?")

    button_login = gwefxp(driver, '/html/body/app-component/div/app-login-component/main/app-login-shared-component'
                                  '/section/form/button')
    button_login.click()


def write_basic_info(driver: WebDriver, info: CompetitionBasicInfo):
    wuvexp(driver, '//*[@id="name"]')

    name_input = gwefxp(driver, '//*[@id="name"]')
    name_input.send_keys(info.name)

    club_input = gwefxp(driver, '//*[@id="clubList"]')
    try:
        Select(club_input).select_by_visible_text(info.club)
    except NoSuchElementException:
        try:
            logging.warning(f"Could not find club '{info.club}', defaulting to first available.")
            Select(club_input).select_by_index(0)
        except NoSuchElementException:
            logging.error("You are part of no clubs.")

    if info.teams:
        teams_input = gwefxp(driver, '//*[@id="isTeam"]')
        teams_input.click()

    if info.desc:
        desc_input = gwefxp(driver, '//*[@id="description"]')
        desc_input.send_keys(info.desc)

    if info.rules:
        rules_input = gwefxp(driver, '//*[@id="rulesUrl"]')
        rules_input.send_keys(info.rules)

    button_next = gwefxp(driver, '/html/body/app-root/app-create-competition-component/app-base-component/div/div/div'
                                 '/div/div[2]/div/button/span[1]')
    button_next.click()
