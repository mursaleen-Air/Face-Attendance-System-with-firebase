import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
   "databaseURL" : "https://faceattendancerealtime-ad241-default-rtdb.asia-southeast1.firebasedatabase.app/"
   


}


)

#importing the images
folderPath = "images"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []

studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    #print(path)
    #print(os.path.splitext(path)[0])
    fileName = os.path.join(folderPath, path) 
            
print(studentIds)



def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList   
print("Encoding Started...")#Encoding started
encodeListKnown = findEncodings(imgList)#Encode generate
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")#Encode Completed

file = open('EncodeFile.p', 'wb')#wb is permissions
pickle.dump(encodeListKnownWithIds, file)
file.close()
print('File Saved')



