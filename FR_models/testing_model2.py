import face_recognition
import os
import pickle

def testing_model2(path):
    names_dic={
        0:"Dallal",
        1:"Ricciardone"
    }

    filename = 'C:/Users/data/PycharmProjects/pythonProject/finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))

    # Load the test image with unknown faces into a numpy array
    test_image = face_recognition.load_image_file(path)

    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        name = model.predict_proba([test_image_enc])

        maxi=max(name[0])
        # print(name,maxi)
        if maxi<0.9:
            print("unknown")
        else:
            res=names_dic[list(name[0]).index(maxi)]
            print(res)
def folder():
    test_dir = os.listdir('C:/Users/data/PycharmProjects/pythonProject/faces/testing_set/')
    for person in test_dir:
        print("hi")
        testing_model2('C:/Users/data/PycharmProjects/pythonProject/faces/testing_set/'  + person)
folder()