from selenium import webdriver
import time
import re

#Goal: should ask for 3 inputs, date, start time, and hours to book for

firstName = "Kevin"
lastName =  "Hu"
email = "kh2547@nyu.edu"
reservationName = "Autorent"
roomList = {} #list of rooms and available hours
roomHourToID = {} #matchup of room+hour to ID
roomTimes = ["9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm","9pm","10pm","11pm", "11:59pm"]
userTimes = [] #hours that the user wants the room rented
roomToRentID = [] #id of each room to rent

driver = webdriver.Chrome()
driver.get("https://nyu.libcal.com/booking/berndibner2")

#day = input("What day do you want to rent? ")
while True:
    startTime = input("What time do you want to rent your room? Please enter number then am/pm. ")
    hours = input("How many hours would you like to rent your room for? ")
    hours = int(hours)
    try:
        startingIndex = roomTimes.index(startTime)
        break
    except ValueError:
        print("That is not a valid time, please try again. (Note: Do not forget am/pm)")

for i in range(hours):
    userTimes.append(roomTimes[i+startingIndex]) #iterate roomTimes to find correct hours

elem = driver.find_elements_by_class_name("lc_rm_a")

for option in elem:
    singleRoomData = option.get_attribute("title") #grab each room data
    singleRoomID = option.get_attribute("id")
    singleRoomData = singleRoomData.replace(',','') #sanitizing string
    singleRoomData = singleRoomData.split()

    key = singleRoomData[2] #roomNum
    value = singleRoomData[3] #room initial time
    if len(value) == 7:
        value = value[0:2] + value[5:7]
    else:
        value = value[0] + value[4:6]

    roomHourToID[key + " " + value] = singleRoomID

    if singleRoomData[2] not in roomList.keys():
        roomList[key] = [value]
    else:
        roomList[key].append(value)

for room,hours in roomList.items():
    if (all([z in hours for z in userTimes])):
        print(room, "has been rented from", userTimes[0]," - ", roomTimes[roomTimes.index(userTimes[-1])+1])
        for i in range (len(userTimes)):
            roomToRentID.append(roomHourToID[room + " " + userTimes[i]])
        break
    #add case for when room is not found here

for id in roomToRentID:
    elem = driver.find_element_by_id(id)
    elem.click()

    #option.click()

time.sleep(0.1)

continueButton = driver.find_element_by_id("rm_tc_cont")
continueButton.click()

firstNameField = driver.find_element_by_id("fname")
firstNameField.send_keys(firstName)

lastNameField = driver.find_element_by_id("lname")
lastNameField.send_keys(lastName)

emailField = driver.find_element_by_id("email")
emailField.send_keys(email)

reservationNameField = driver.find_element_by_id("nick")
reservationNameField.send_keys(reservationName)

submitButton = driver.find_element_by_id("s-lc-rm-sub")
submitButton.click()
#driver.close()

