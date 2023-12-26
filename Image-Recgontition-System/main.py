import cv2
import tkinter
from tkinter import messagebox
from tkinter.simpledialog import askstring
import numpy as np
import os
from PIL import Image
import face_recognition as fr

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def read_credentials():
    global file_username, file_password
    username_file = open('user-pass/username','r')
    file_username = username_file.readline()
    username_file.close()
    password_file = open('user-pass/password','r')
    file_password = password_file.readline()
    password_file.close()
read_credentials()


admin_names = []
admin_paths = []

def include_admin_data():
    global admin_paths, admin_names
    faces_path = "D:\\PROGRAMS\\OPEN CV\\Image Recognition System\\admin_face"
    admin_names= []
    admin_paths = []
    admin_names = os.listdir(f"{faces_path}")
    for i , name in enumerate(admin_names):
        face= fr.load_image_file(f"{faces_path}\\{name}")
        admin_paths.append(fr.face_encodings(face)[0])
        admin_names[i] = name.split(".")[0]
include_admin_data()



def new_user():
    user_name = askstring("Name","What is your name ? ")
    if("" != user_name and user_name != None):
        messagebox.showinfo("Hello", "Hi! {}".format(user_name))    
        face_adder(user_name)

def face_adder(face_name):
    count_faces = 1
    cap = cv2.VideoCapture(0)
    tkinter.messagebox.showinfo("Face Update", f"Hi! {face_name}\nLook straight towards camera")
    if face_name == "Admin":
        foldername = "admin"
    else:
        foldername = "user"
    while True:
        _ , img = cap.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1,4)
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            face = gray[y : y+h, x : x+w]
            filename = f'D:\\PROGRAMS\\OPEN CV\\Image Recognition System\\{foldername}_face\\'+ face_name+'_'+str(count_faces)+'.jpg'
            cv2.imwrite(filename, face)
            count_faces+=1
        cv2.putText(img,str(count_faces),(50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
        cv2.imshow('Face Detector', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27 or count_faces > 10:   
            cap.release()
            cv2.destroyWindow('Face Detector')
            if(foldername == "admin"):
                messagebox.showinfo("UPDATING","Please wait for few seconds\nAdmin is being updated")
                login_window.tkraise()
            return 
        
def recogniser():
    faces_path = "D:\\PROGRAMS\\OPEN CV\\Image Recognition System\\user_face"
    names = os.listdir(f"{faces_path}")
    paths = []
    for i , name in enumerate(names):
        face= fr.load_image_file(f"{faces_path}\\{name}")
        paths.append(fr.face_encodings(face)[0])
        names[i] = name.split(".")[0]
    cap = cv2.VideoCapture(0)
    while True:
        _,img = cap.read()
        imgS = cv2.resize(img,(0,0),None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = fr.face_locations(imgS)
        encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)
        
        for encodeFace , faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = fr.compare_faces(paths, encodeFace)
            faceDis = fr.face_distance(paths, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = names[matchIndex].upper()
                name = "".join(name.split("_")[0])
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img, name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        cv2.imshow("Face Recognition", img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cap.release()
            cv2.destroyWindow('Face Recognition')
            return 




def check_admin():
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        _,img = cap.read()
        imgS = cv2.resize(img,(0,0),None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = fr.face_locations(imgS)
        encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)
        
        for encodeFace , faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = fr.compare_faces(admin_paths, encodeFace)
            faceDis = fr.face_distance(admin_paths, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = admin_names[matchIndex].upper()
                name = "".join(name.split("_")[0])
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img, name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cap.release()
                return True
        # cv2.imshow("Face Recognition", img)
        count+=1
        if count > 10 :
            cap.release()
            # cv2.destroyWindow('Face Recognition')
            return False


def check_credential(face_result , face_check_done,is_setting):
    if(not is_setting):
        if(not face_check_done):
            username = username_entry.get()
            password = password_entry.get()
            if username == file_username and password == file_password:
                messagebox.showinfo("Valid", "Welcome")
                main_window.tkraise()
            else:
                messagebox.showerror("Invalid","Username or Password is incorrect")
        else:
            if(face_result):
                messagebox.showinfo("Valid", "Welcome")
                main_window.tkraise()
            else:
                messagebox.showerror("Invalid", "User can't be identified")
    else:
        username = settings_username_entry.get()
        password = settings_password_entry.get()
        if username == file_username and password == file_password:
            messagebox.showinfo("Valid", "Welcome")
            settings_window_frame2.tkraise()
        else:
            messagebox.showerror("Invalid","Username or Password is incorrect")


def check_updated_credential(a):
    if(a == "username"):
        s1 = username_update_window_entry.get()
        s2 = username_update_window_confirm_entry.get()
        if(s1 == s2):
            f = open("user-pass/username",'w')
            f.write(s1)
            f.close()
            messagebox.showinfo("Done", "Username is updated")
            read_credentials()
            settings_window.tkraise()
        else:
            messagebox.showerror("Error", "Username are not same")
    else:
        s1 = password_update_window_entry.get()
        s2 = password_update_window_confirm_entry.get()
        if(s1 == s2):
            f = open("user-pass/password",'w')
            f.write(s1)
            f.close()
            read_credentials()
            messagebox.showinfo("Done","Password is updated")
            settings_window.tkraise()
        else:
            messagebox.showerror("Error", "Psssword are not same")

################## CONTAINER WINDOW ##########################################
container = tkinter.Tk()
container.attributes("-fullscreen",True)


################################ SETTINGS WINDOW ###########################################
settings_window = tkinter.Frame(container, bg= "#A1A1A1", height = 785 , width = 1540)
settings_window.place(x= 0, y = 82)

settings_window_frame = tkinter.Frame(settings_window, width  = 1200, height = 600, bg = "#D1D1D1")
settings_window_frame.place(x = 160, y = 100)

settings_label = tkinter.Label(settings_window_frame, text = "LOGIN", font = ("Freedom", 60),bg = "#D1D1D1")
settings_label.place(x = 500, y = 25)

settings_username_label = tkinter.Label(settings_window_frame, text = "User name", font = ("Freedom", 30), bg="#D1D1D1")
settings_username_label.place(x = 200, y = 150)

settings_username_entry = tkinter.Entry(settings_window_frame, font = ("Freedom", 35),width = 20)
settings_username_entry.place(x = 500, y = 150)

settings_password_label = tkinter.Label(settings_window_frame, text = "Password", font = ("Freedom", 30), bg = "#D1D1D1")
settings_password_label.place(x = 200, y = 230)

settings_password_entry = tkinter.Entry(settings_window_frame, font = ("Freedom", 35), width = 20,show = "\u2022")
settings_password_entry.place(x = 500, y = 230)

settings_submit_button = tkinter.Button(settings_window_frame, text = "Submit", font =("Freedom", 30), command = lambda : check_credential(False, False,True))
settings_submit_button.place(x = 350 , y = 350)

clear_button = tkinter.Button(settings_window_frame, text = "Clear", font = ("Freedom", 30), command = lambda : [settings_username_entry.delete(0,tkinter.END), settings_password_entry.delete(0,tkinter.END)])
clear_button.place(x = 600, y= 350)

logout_button = tkinter.Button(settings_window_frame, text = "Close", font = ("Freedom", 35),bg = "red", command= lambda : main_window.tkraise())
logout_button.place(x = 50, y = 500)



##################################### PASSWORD UPDATE WINDOW ##################################

password_update_window = tkinter.Frame(container,bg= "#A1A1A1", height = 785 , width = 1540)
password_update_window.place(x= 0, y = 82)

password_update_window_label = tkinter.Label(password_update_window, text= "New Password", font = ("Freedom", 35),bg = "#A1A1A1" )
password_update_window_label.place(x = 300, y = 300)

password_update_window_entry = tkinter.Entry(password_update_window, font = ("Freedom", 35) )
password_update_window_entry.place(x = 850, y = 300)

password_update_window_confirm_label = tkinter.Label(password_update_window, text= "Confirm Password", font = ("Freedom", 35),bg = "#A1A1A1" )
password_update_window_confirm_label.place(x = 300, y = 350)

password_update_window_confirm_entry = tkinter.Entry(password_update_window, font = ("Freedom", 35) )
password_update_window_confirm_entry.place(x = 850, y = 350)

password_username_submit_button = tkinter.Button(password_update_window, text = "Submit", font =("Freedom", 30), command = lambda : check_updated_credential("password"))
password_username_submit_button.place(x = 450 , y = 450)

password_username_clear_button = tkinter.Button(password_update_window, text = "Clear", font = ("Freedom", 30), command = lambda : [settings_username_entry.delete(0,tkinter.END), settings_password_entry.delete(0,tkinter.END)])
password_username_clear_button.place(x = 800, y= 450)
######################################## USERNAME UPDATE ##############################################

username_update_window = tkinter.Frame(container,bg= "#A1A1A1", height = 785 , width = 1540)
username_update_window.place(x= 0, y = 82)

username_update_window_label = tkinter.Label(username_update_window, text= "New Username", font = ("Freedom", 35),bg = "#A1A1A1" )
username_update_window_label.place(x = 300, y = 300)

username_update_window_entry = tkinter.Entry(username_update_window, font = ("Freedom", 35) )
username_update_window_entry.place(x = 850, y = 300)

username_update_window_confirm_label = tkinter.Label(username_update_window, text= "Confirm Username", font = ("Freedom", 35),bg = "#A1A1A1" )
username_update_window_confirm_label.place(x = 300, y = 350)

username_update_window_confirm_entry = tkinter.Entry(username_update_window, font = ("Freedom", 35) )
username_update_window_confirm_entry.place(x = 850, y = 350)

update_username_submit_button = tkinter.Button(username_update_window, text = "Submit", font =("Freedom", 30), command = lambda : check_updated_credential("username"))
update_username_submit_button.place(x = 450 , y = 450)

update_username_clear_button = tkinter.Button(username_update_window, text = "Clear", font = ("Freedom", 30), command = lambda : [settings_username_entry.delete(0,tkinter.END), settings_password_entry.delete(0,tkinter.END)])
update_username_clear_button.place(x = 800, y= 450)

#####################################SETTINGS FRAME2 UPDATE ####################################

settings_window_frame2 = tkinter.Frame(container, bg= "#A1A1A1", height = 785 , width = 1540)
settings_window_frame2.place(x= 0, y = 82)

update_admin_button = tkinter.Button(settings_window_frame2, text = "Update Admin", font = ("Freedom", 35), activebackground="green", command = lambda : [face_adder('Admin'), include_admin_data()])
update_admin_button.place(x= 50, y = 200)

change_password = tkinter.Button(settings_window_frame2, text = "Change Password", font = ("Freedom", 35),command = lambda : password_update_window.tkraise())
change_password.place(x = 50 , y = 300)

change_username = tkinter.Button(settings_window_frame2, text = "Change Username", font = ("Freedom", 35),command = lambda : username_update_window.tkraise())
change_username.place(x = 50 , y = 400)

change_logout_button = tkinter.Button(settings_window, text = "Logout", font = ("Freedom", 35),bg = "red", command= lambda : login_window.tkraise())
change_logout_button.place(x = 1360, y = 830)

################################## MAIN LABEL ######################################
Heading = tkinter.Label(container, text = "Face Recognition System", font = ("Debrosee", 55),relief = "raised" ,bg = "#000000", fg = "#A1A1A1",width = 39)
Heading.place(x= 0,y = 0)


################################## MAIN WINDOW FRAME #####################################
main_window = tkinter.Frame(container, bg = "#A1A1A1",height = 785, width = 1540)
main_window.place(x = 0,y = 82)

face_recognise_button = tkinter.Button(main_window, text = "Recognise", font = ("Freedom", 35), activebackground="green", command = lambda : recogniser())
face_recognise_button.place(x= 50, y =200)

add_user_button = tkinter.Button(main_window, text = "Add New Person", font = ("Freedom", 35), activebackground="green", command = lambda : new_user())
add_user_button.place(x= 50, y =300)

settings_button = tkinter.Button(main_window, text = "Settings",font = ("Freedom", 35),command = lambda : settings_window.tkraise()) 
settings_button.place(x = 50 , y = 400)

logout_button = tkinter.Button(main_window, text = "Logout", font = ("Freedom", 35),bg = "red", command= lambda : login_window.tkraise())
logout_button.place(x = 50, y = 500)


###################################### LOGIN WINDOW ############################################
login_window = tkinter.Frame(container, bg = "#A1A1A1", height = 785, width = 1540)
login_window.place(x =0, y = 82)

##################################### lOGIN FRAME ##############################################
login_frame = tkinter.Frame(login_window, width  = 1200, height = 600, bg = "#D1D1D1")
login_frame.place(x = 160, y = 100)

login_label = tkinter.Label(login_frame, text = "LOGIN", font = ("Freedom", 60),bg = "#D1D1D1")
login_label.place(x = 500, y = 25)

username_label = tkinter.Label(login_frame, text = "User name", font = ("Freedom", 30), bg="#D1D1D1")
username_label.place(x = 200, y = 150)

username_entry = tkinter.Entry(login_frame, font = ("Freedom", 35),width = 20)
username_entry.place(x = 500, y = 150)

password_label = tkinter.Label(login_frame, text = "Password", font = ("Freedom", 30), bg = "#D1D1D1")
password_label.place(x = 200, y = 230)

password_entry = tkinter.Entry(login_frame, font = ("Freedom", 35), width = 20,show = "\u2022")
password_entry.place(x = 500, y = 230)

submit_button = tkinter.Button(login_frame, text = "Submit", font =("Freedom", 30), command = lambda : check_credential(False, False,False))
submit_button.place(x = 350 , y = 350)

clear_button = tkinter.Button(login_frame, text = "Clear", font = ("Freedom", 30), command = lambda : [username_entry.delete(0,tkinter.END), password_entry.delete(0,tkinter.END)])
clear_button.place(x = 600, y= 350)

face_scan_login_button = tkinter.Button(login_frame, text = "Scan using Face ID", font = ("Freedom", 30),command = lambda : check_credential(check_admin(), True,False))
face_scan_login_button.place(x = 320, y = 420)

######################################## QUIT BUTTON #########################################
quitbutton = tkinter.Button(login_window, text = "Quit", font = ("Freedom", 30),bg = "red", command = lambda : quit())
quitbutton.place(x = 1380, y = 730)




container.mainloop()