import cv2
import os
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/background.png")
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)#we made a list of the files present in this directory

imgModeList = []
#importing the mode images into a list
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
print(modePathList)
while True:
    success, img = cap.read()

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808+414] = imgModeList[0]
    #cv2.imshow("Face Attendance", img)
    cv2.imshow("Webcam", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
