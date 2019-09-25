from selenium import webdriver
import time
#import pandas

#Goal: should ask for 3 inputs, date, start time, and hours to book for
#list of room list, inside each room list, string with starting time

roomList = {}

driver = webdriver.Chrome()
driver.get("https://nyu.libcal.com/booking/berndibner2")

elem = driver.find_elements_by_class_name("lc_rm_a")
time.sleep(1)

#possibly map id to date to figure out what to click
for option in elem:
    roomData = (option.get_attribute("title")).split()
    key = roomData[2]
    value = roomData[3]
    if roomData[2] not in roomList.keys():
        roomList[key] = [value]
    else:
        roomList[key].append(value)

    #option.click()

driver.close()

print(roomList)