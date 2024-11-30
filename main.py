import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
   "databaseURL" : "https://faceattendancerealtime-ad241-default-rtdb.asia-southeast1.firebasedatabase.app/"
   


}
)
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

modeType = 0

counter = 0
id = -1
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)#we are resizing imgS
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
     


    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808+414] = imgModeList[modeType]
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
            id = studentIds[matchIndex]
            
            if counter == 0:
                counter =1
                modeType = 1 #When the face matches we want it to change from active to 2nd modetype .

    if counter != 0:
        if  counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
        cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1 )
        
        cv2.putText(imgBackground, str(studentInfo['name']), (808, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )

        
        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )
        
        cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )
        
        
        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )
        
        cv2.putText(imgBackground, str(studentInfo['semester']), (1025, 625 ), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )
        
        
        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) , 1 )
        
        
        counter+=1            
    cv2.imshow("Webcam", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
