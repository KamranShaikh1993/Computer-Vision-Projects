import csv
import cv2
from datetime import datetime
import face_recognition
import glob
import numpy as np
import os
import pandas as pd
import sqlite3 , csv



try:
    def func1():

        video_capture = cv2.VideoCapture(0)


        # Read multiple images from a folder
        X = []
        b = []
        known_faces_encoding = []
        known_faces_names = []

        path ='Photos\*.*'   # folder\*.*   * all files and .* any extension
        print(path)
        for file in glob.glob(path):
            print(file)
            # to read image from file one by one
            img = cv2.imread(file)
            X.append(file)
            known_faces_encoding.append(face_recognition.face_encodings(img)[0])

        # Retrive only names
        for i in X:
            a = i[7:-4]
            b.append(a)
        #    print('Retrive only names :',b)

        # Names by index
            
        j=0
        for i in b:
        #     print('Names by index',b[j])
            known_faces_names.append(b[j])
            j+=1
            
            
        students = known_faces_names.copy()

        # The following variables will be used for face which is coming from webcam

        face_locations = []      # face coordinates
        face_encodings = []      # face_encoding is raw data
        face_names = []          # name of face if it's present in the above list
        s = True

        # current date
        now = datetime.today()              # fetch current date and time
        current_date = now.strftime('%Y-%m-%d') # get only date
        current_time = now.strftime('%H:%M:%S') # get only current_time



        Std_Name = []
        Attendance_time = []
        Absent = []


        while True:
            _,frame = video_capture.read()
            small_frame = cv2.resize(frame,(0,0),fx = 0.25, fy =0.25)
            rgb_small_frame = small_frame[:,:,::-1]
            if s:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_faces_encoding, face_encoding)
                    name = ''
                    face_distance = face_recognition.face_distance(known_faces_encoding, face_encoding)
                    best_match_index = np.argmin(face_distance)
                    if matches[best_match_index]:
                        name = known_faces_names[best_match_index]
                        #Std_Name.append(name)
                        
                        
                    face_names.append(name)
                    if name in known_faces_names:
                        if name in students:
                            # List for Student name
                            Std_Name.append(name)
                            # List for Attendance time
                            Attendance_time.append(current_time)
                            students.remove(name)
                            print(students)
                        
                            

                            
            cv2.imshow('Attendance_System',frame)
            if cv2.waitKey(5)==ord('q'):
                break
                

        # Create list for Absent column        
        Absent.extend(students)

        i=0
        #while i in range(0,len(Std_Name)):
        for j in Std_Name:
            Absent.append(np.nan)

            i+=1      

        Absent = Absent[0:-1]

        # Creating DataFrame
        df = pd.DataFrame({'Student_Name':Std_Name, 'Attendance_Time':Attendance_time, 'Absent_Students':Absent})


        # Create a csv file
        df.to_csv(current_date + '_New' + '.csv')



                
        video_capture.release()    # TO close the video
        cv2.destroyAllWindows()    # To close all windows
        
        return df


    def func2(A):
        # DataBase

        df = pd.read_csv('2023-03-25_New.csv')
        print(df.head())


        # Drop Selected Columns
        df1 = df.drop([ 'Unnamed: 0' ], axis=1)
        df1.to_csv('2023-03-25_New1.csv', index=False)

        return df1


    def func3(B):

        # # Connect to DB and create a cursor

        connection = sqlite3.connect('Attendance.db')
        cursor = connection.cursor()

        print('DB Init')

        # Write a query and execute it with cursor

        query = 'select sqlite_version();'
        cursor.execute(query)

        # Fetch and output result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result))


        d = os.getcwd()
        fname = os.path.join(d,'2023-03-25_New1.csv')

        
        with open(fname, mode ='r')as file:
        
            # reading the CSV file
            csvFile = csv.reader(file)
        
            no_records = 0
            for row in file:
                cursor.execute('INSERT into Std_Attendance values(?,?,?)',row.split(','))
                connection.commit()
                no_records+=1
        cursor.close()

        connection.close()
        print('SQLite connection closed')
except:
    print("Something went wrong")

if __name__=='__main__':
    A = func1()
    B = func2(A)
    C = func3(B)