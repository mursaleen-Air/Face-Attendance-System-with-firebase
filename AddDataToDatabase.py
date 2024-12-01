import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{

'databaseURL':"https://faceattendancerealtime-ad241-default-rtdb.asia-southeast1.firebasedatabase.app/"


})

ref = db.reference('Students')
data = {
   "231213":
        {
            "name":"Muhammad Mursaleen",
            "major":"BSAI",
            "starting_year":2023,
            "total_attendance":6,
            "standing":"G",
            "semester":"3",
            "last_attendance_time":"2024-11-30 00:54:34"



        },
    "321654":
       {
            "name":"Murtaza Hassan",
            "major":"Robotics",
            "starting_year":2017,
            "total_attendance":6,
            "standing":"G",
            "semester":"3",
            "last_attendance_time":"2024-11-30 00:54:34"




       },
      "852741":
       {
            "name":"Emily Blunt",
            "major":"Economics",
            "starting_year":2018,
            "total_attendance":17,
            "standing":"B",
            "semester":"7",
            "last_attendance_time":"2024-11-30 00:54:34"




       },
       "963852":
       {
            "name":"Elon Musk",
            "major":"Physics",
            "starting_year":2020,
            "total_attendance":8,
            "standing":"G",
            "semester":"3",
            "last_attendance_time":"2024-11-30 00:54:34"




       }, 

}

for key,value in data.items():
    ref.child(key).set(value)