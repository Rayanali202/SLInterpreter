import cv2
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector()

tips = [4,8,12,16,20]
fingers = [0]

#returns list containing information on fingers
#first five spots represent whether each finger is raised
#last four spots show if tips of the index to pinky fingers have
#the same X coordinate value as the thumb
def getFingers(myList, tipList):
    fingersList = []
    for tip in tipList:
        if myList[tip][2] < myList[tip - 2][2]:
            fingersList.append(1)
        else:
            fingersList.append(0)

    for tip in tipList:
        if tip != 4:
            if abs(myList[4][1] - myList[tip][1]) < 20:
                fingersList.append(1)
            else:
                fingersList.append(0)

    return fingersList

alphabet = {"[1, 0, 0, 0, 0, 0, 0, 0, 0]":'A',
            "[1, 1, 1, 1, 1, 0, 0, 1, 0]":'B',
            "[1, 1, 1, 1, 1, 1, 1, 1, 1]":'C',
            "[1, 1, 0, 0, 0, 0, 1, 0, 0]":'D',
            "[1, 0, 0, 0, 0, 0, 0, 0, 1]":'E',
            "[1, 0, 1, 1, 1, 1, 0, 0, 0]":'F',
            "[1, 1, 0, 0, 0, 1, 0, 0, 0]":'G',
            "[1, 1, 1, 0, 0, 0, 0, 0, 0]":'H',
            "[1, 0, 0, 0, 1, 0, 0, 1, 0]":'I',
            "[0, 1, 1, 1, 0, 0, 0, 0, 0]":'J',
            "[1, 1, 1, 0, 0, 1, 0, 0, 0]":'K',
            "[1, 1, 0, 0, 0, 0, 0, 0, 0]":'L',
            "[1, 0, 0, 0, 0, 1, 0, 0, 0]":'M',
            "[1, 0, 0, 0, 0, 0, 0, 1, 0]":'N',
            "[1, 0, 0, 0, 0, 1, 1, 1, 1]":'O',
            "[1, 1, 0, 0, 0, 1, 1, 0, 0]":'P',
            "[0, 0, 1, 1, 1, 0, 0, 0, 0]":'Q',
            "[1, 1, 1, 0, 0, 0, 0, 1, 0]":'R',
            "[1, 0, 0, 0, 0, 0, 1, 0, 0]":'S',
            "[1, 0, 0, 0, 1, 0, 1, 0, 0]":'T',
            "[1, 1, 1, 0, 0, 0, 0, 0, 1]":'U',
            "[0, 1, 1, 0, 0, 0, 0, 0, 0]":'V',
            "[1, 1, 1, 1, 0, 0, 0, 0, 1]":'W',
            "[1, 1, 0, 0, 0, 0, 1, 1, 1]":'X',
            "[1, 0, 0, 0, 1, 0, 0, 0, 0]":'Y',
            "[1, 1, 1, 1, 1, 0, 0, 0, 0]":'Z'}
oldLetter = '0'
counter = 0
updatedList = [0]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    counter += 1

    #checks if finger formation is in alphabet then prints
    if len(lmList) != 0 and counter == 5:
        updatedList = getFingers(lmList,tips)
        if fingers != updatedList:
            fingers = updatedList

            tempKey = str(fingers)
            if tempKey in alphabet:
                newLetter = alphabet[tempKey]
                if newLetter != oldLetter:
                    print(alphabet[tempKey])
                    oldLetter = newLetter

    if counter == 5:
        counter = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)