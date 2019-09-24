from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://nyu.libcal.com/booking/berndibner2")


elem = driver.find_elements_by_class_name("lc_rm_a")
elem2 = driver.find_elements_by_class_name("ui-state-default")
time.sleep(1)

#possibly map id to date to figure out what to click
for option in elem:
    print(option.get_attribute("title"))

    #option.click()

driver.close()