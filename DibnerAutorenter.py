from selenium import webdriver
import selenium.common.exceptions
import datetime
import time

currentDT = datetime.datetime.now()


firstName = "Kevin"
lastName =  "Hu"
email = "kh2547@nyu.edu"
reservationName = "Autorent"
roomList = {} #list of rooms and available hours
roomHourToID = {} #matchup of room+hour to html ID
roomTimes = ["9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm","9pm","10pm","11pm", "11:59pm"]
userTimes = [] #hours that the user wants the room rented
roomToRentID = [] #id of each room to rent
now = datetime.datetime.now()

driver = webdriver.Chrome()
driver.get("https://nyu.libcal.com/booking/berndibner2")

dayFound = False
while (True):
    day = input("What day do you want to rent? Enter blank for current day. ")
    if (day == ''):
        day = now.day
        break
    dateTable = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[*]/td[*]")
    for dateButton in dateTable:
        if (dateButton.text == day):
            dateButton.click() #click on specific day table on website
            dayFound = True
            break
    if (dayFound == False):
        print("The day you entered was invalid, please enter another day.")
    else:
        break

while True:
    startTime = input("What time do you want to rent your room? Please enter number then am/pm. ")

    try:
        startingIndex = roomTimes.index(startTime)
        break
    except ValueError:
        print("That is not a valid time, please try again. (Note: Do not forget am/pm)")
        continue

while True:
    hours = input("How many hours would you like to rent your room for? ")
    try:
        hours = int(hours)
    except ValueError:
        print("This is an invalid number of hours. Please enter a valid number. ")
        continue
    if (hours > 3 or hours < 1):
        print("Rooms cannot be booked for more than 3 hours and must be at least 1 hour.")
        continue
    break

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