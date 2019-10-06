from selenium import webdriver
import selenium.common.exceptions
import datetime
import time
import imaplib
import email


currentDT = datetime.datetime.now()

firstName = "Kevin"
lastName =  "Hu"
userEmail = "kh2547@nyu.edu"
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

driver.find_element_by_id("rm_tc_cont").click()
driver.find_element_by_id("fname").send_keys(firstName)
driver.find_element_by_id("lname").send_keys(lastName)
driver.find_element_by_id("email").send_keys(userEmail)
driver.find_element_by_id("nick").send_keys(reservationName)
driver.find_element_by_id("s-lc-rm-sub").click()

driver.close()

time.sleep(20)

with open("email_Info.txt","r") as emailInfo:
    emailAddress = emailInfo.readline()
    emailPassword = emailInfo.readline()

mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
mail.login(emailAddress, emailPassword)
mail.select("inbox")

type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]

raw_email_string = raw_email.decode('utf-8')
email_message = email.message_from_string(raw_email_string)

if email_message.is_multipart():
    for part in email_message.get_payload():
        confirmAddress = (part.get_payload(decode=True).decode('utf-8')).split('\r\n')[3]
        print(confirmAddress)
        break;

driver = webdriver.Chrome()
driver.get(confirmAddress)
driver.find_element_by_id('rm_confirm_link').click()