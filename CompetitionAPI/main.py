from selenium.webdriver.chrome import webdriver

from utils.create_competition import *
from utils.forms import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://admin.trackmania.nadeo.club/create/competition")

    login(driver)

    comp_info = CompetitionBasicInfo(
        "test_comp",
        "Nixoticlub",
        False,
        "My test comp"
    )
    write_basic_info(driver)