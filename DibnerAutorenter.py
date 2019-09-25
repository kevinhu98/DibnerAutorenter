from selenium import webdriver
import time
import re

#Goal: should ask for 3 inputs, date, start time, and hours to book for

roomList = {}
roomTimes = ["9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm","9pm","10pm","11pm"]
userTimes = [] #hours that the user wants the room rented

#day = input("What day do you want to rent? ")
startTime = input("What time do you want to rent your room? Please enter number then am/pm. ")
hours = input("How many hours would you like to rent your room for? ")
hours = int(hours)

startingIndex = roomTimes.index(startTime)
for i in range(hours):
    userTimes.append(roomTimes[i+startingIndex]) #iterate roomTimes to find correct hours

print(userTimes)
driver = webdriver.Chrome()
driver.get("https://nyu.libcal.com/booking/berndibner2")

elem = driver.find_elements_by_class_name("lc_rm_a")
time.sleep(2) #delay to load page

for option in elem:
    singleRoomData = option.get_attribute("title") #grab each room data
    singleRoomData = singleRoomData.replace(',','') #grab
    singleRoomData = singleRoomData.split()
    key = singleRoomData[2] #roomID
    value = singleRoomData[3] #room initial time
    print(singleRoomData)
    if len(value) == 7:
        value = value[0:2] + value[5:7]
    else:
        value = value[0] + value[4:6]

    if singleRoomData[2] not in roomList.keys():
        roomList[key] = [value]
    else:
        roomList[key].append(value)


foundRoom = False
#while (foundRoom != True):

    #option.click()

driver.close()

print(roomList)