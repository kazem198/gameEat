import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import os
import cvzone
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = FaceMeshDetector(maxFaces=1)


pathEatAble = "Objects/eatable"
EatAble = os.listdir(pathEatAble)
listEatAble = []
for eat in EatAble:
    img = cv2.imread(f'{pathEatAble}/{eat}', cv2.IMREAD_UNCHANGED)
    listEatAble.append(img)

pathNoneEatAble = "Objects/noneatable"
NoneEatAble = os.listdir(pathNoneEatAble)
listNoneEatAble = []
for NoneEat in NoneEatAble:
    img = cv2.imread(f'{pathNoneEatAble}/{NoneEat}', cv2.IMREAD_UNCHANGED)
    listNoneEatAble.append(img)

y = 0
x = 500
closeMouth = True
prize = 0
gameOver = False


def update(x, y):
    y = 0
    x = random.randint(100, 1100)
    return x, y


currentImg = listNoneEatAble[0]

global choiseEatAble
choiseEatAble = False


def choiseImg():
    global choiseEatAble
    eatAbleOrNoneEatAble = random.randint(0, 3)

    if (eatAbleOrNoneEatAble != 0):
        currentImg = listEatAble[random.randint(0, 3)]
        choiseEatAble = True

    else:
        currentImg = listNoneEatAble[random.randint(0, 3)]
        # print("bash")
        choiseEatAble = False

    return currentImg


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    if gameOver == False:
        img, face = detector.findFaceMesh(img, draw=False)
        y += 10
        if face:
            face = face[0]
            cv2.circle(img, (face[0]), 5, (255, 0, 0), 5)  # up
            cv2.circle(img, (face[17]), 5, (255, 0, 0), 5)  # down
            cv2.circle(img, (face[78]), 5, (255, 0, 0), 5)  # left
            cv2.circle(img, (face[292]), 5, (255, 0, 0), 5)  # right

            cv2.line(img, face[0], face[17], (0, 255, 0), 3)
            cv2.line(img, face[78], face[292], (0, 255, 0), 3)

            cx, cy = int((face[78][0]+face[292][0]) //  # center of mouth
                         2), int((face[78][1]+face[292][1])//2)

            distanceMouth, _ = detector.findDistance(face[0], face[17])

            if distanceMouth < 50:
                closeMouth = True
                cv2.putText(img, "close", (50, 50),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            else:
                closeMouth = False
                cv2.putText(img, "open", (50, 50),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.circle(img, (cx, cy), 2, (0, 0, 255), 5)

            if (y > 650):

                x, y = update(x, y)
                currentImg = choiseImg()

            else:

                cvzone.overlayPNG(img, currentImg, (x, y))
                cv2.line(img, (cx, cy), (x+50, y+50), (0, 0, 255), 3)

            disEat, _ = detector.findDistance((cx, cy), (x+50, y+50))
            if disEat < 50 and closeMouth == False:
                if choiseEatAble:
                    x, y = update(x, y)
                    currentImg = choiseImg()

                    prize += 1
                else:
                    gameOver = True

        cv2.putText(img, str(prize), (1150, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    else:
        cv2.putText(img, "game over", (200, 500),
                    cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 5)
        cv2.putText(img, "to start again press r", (50, 600),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 5)

    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key & 0xff == ord("q"):
        cv2.destroyAllWindows()
        break
    elif key == ord("r"):
        y = 0
        x = 500
        gameOver = False
        prize = 0
        choiseEatAble = False
        currentImg = listNoneEatAble[3]
