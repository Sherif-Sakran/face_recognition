import face_recognition
import cv2
import os
from model1 import *
import re

margin = 20

def pre_processing(img):
    img=cv2.imread(img)

    return img

def get_faces(img):
    img = pre_processing(img)
    face_locations = face_recognition.face_locations(img)
    face_dic5 = {}
    i=1

    for (top, right, bottom, left) in face_locations:
        face_dic5["X" + str(i)] = (top,bottom,left,right)

        img=cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(img, "X" + str(i), (left,top), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)
        i += 1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return face_dic5,img
def file_count(dir_path):
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count
def add_to_dir(name,img,path):

    fpath=path+'/faces/training_set/' + str(name)

    isDirectory = os.path.isdir(fpath)
    if not isDirectory:
        os.mkdir(fpath)
        print(name+" created")

        cv2.imwrite(os.path.join(fpath, name +str(1)+ ".jpg"), img)
    else:

        count = file_count(fpath)
        print(name + str(count + 1) + " added")
        cv2.imwrite(os.path.join(fpath, name + str(count + 1) + ".jpg"), img)


#tag(face_dic, person_var,paths[counter])
def tag(face_dict6,name,imgg):
    path=re.findall(".*\/",imgg)[0]
    print(0,path)
    path = re.findall(".*\/", path[:-1])[0]
    print(1,path)
    img = pre_processing(imgg)
    img2 = pre_processing(imgg)
    for i in range(len(face_dict6)):
        (top,bottom,left,right)=face_dict6["X"+str(i+1)]
        img1 = img2[top-margin:bottom+margin, left-margin:right+margin, :]
        add_to_dir(name[i], img1,path)

        cv2.putText(img, name[i], (left,top), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
        img = cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        build_encodings(path+'/faces/training_set/'
                        + str(name[i]),
                        5)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def reco(coordinates,name,imgg):


    (top,bottom,left,right)=coordinates


    cv2.putText(imgg, name, (left,top), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 255, 255), 4, cv2.LINE_AA)
    img = cv2.rectangle(imgg, (left, top), (right, bottom), (0, 0, 255), 2)




    return img