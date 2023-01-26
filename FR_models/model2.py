import os
import face_recognition
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle

# The training data would be all the face encodings from all the known images and the labels are their names
def data_processing():
    data={
        "names":{}
    }
    for i in range(128):
        data["pixel"+str(i)]={}

    # Training directory
    train_dir = os.listdir('C:/Users/data/PycharmProjects/pythonProject/faces/training_set/')

    count=0
    # Loop through each person in the training directory
    for person in train_dir:
        print("hi")
        pix = os.listdir("C:/Users/data/PycharmProjects/pythonProject/faces/training_set/" + person)

        # Loop through each training image for the current person
        for person_img in pix:
            print("hi2")
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file("C:/Users/data/PycharmProjects/pythonProject/faces/training_set/" + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                face_enc = face_enc.flatten()
                for i in range(len(face_enc)):
                    data["pixel"+str(i)][count]=(face_enc[i])
                    data["names"][count]=(person)
                count+=1

            else:
                print(person + "/" + person_img + " was skipped and can't be used for training")
    df=pd.DataFrame(data, columns=data.keys())
    df.to_csv("C:/Users/data/PycharmProjects/pythonProject/data")


def model():
    df = pd.read_csv("C:/Users/data/PycharmProjects/pythonProject/data")

    LE = LabelEncoder()
    df['names'] = LE.fit_transform(df['names'])
    pixels = df.iloc[:, 2:]
    names = list(df["names"])

    model = MLPClassifier(random_state=1, max_iter=300).fit(pixels.values, names)
    filename = 'C:/Users/data/PycharmProjects/pythonProject/finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))
data_processing()
model()