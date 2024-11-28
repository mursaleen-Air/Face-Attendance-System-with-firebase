import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
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
#print(modePathList)

#Load the encoding file
print("Loading Encoded File ...")
file = open('EncodeFile.p', 'rb') #rb is for reading
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#    print(studentIds)
print("Encode File Loaded...")
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)#we are resizing imgS
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
     


    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808+414] = imgModeList[0]
    #cv2.imshow("Face Attendance", img)
    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame ):#This for loop matches the face on the webacam with already present images 
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print("matches", matches)
        #print("faceDis", faceDis)

    matchIndex = np.argmin(faceDis)
    print("Match Index", matchIndex)


    if matches[matchIndex]:#if matches at matchInqdex is true ,
        #print("Known Face Detected")
        y1, x2,y2,x1 = faceLoc
        y1 ,x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 
        bbox = 55 + x1, 162 + y1, x2 -x1, y2 - y1
        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0 )

    cv2.imshow("Webcam", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
