import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from main import *
from model1 import *
import face_recognition
import pickle
import glob
from read_encodings import read_encodings
import pandas as pd
import re
import cv2
import webbrowser

counter = 0
images = []
paths = []
face_dict = []
img_w = 300
img_h = 300

imgColSpan = 3
imgRowSpan = 14

def reset():
    global nameLabel, counterLabel,button_backward, button_forward, counter, images, paths,face_dict

    # if operated_once:
    img.grid_forget()
    nameLabel.grid_forget()
    counterLabel.grid_forget()
    button_backward['state'] = DISABLED
    button_forward['state'] = DISABLED
    counter = 0
    images = []
    paths = []
    face_dict = []



    global saveButton, infoLabel, saveButton, personNameLabel, personNameEntry
    global authorLabel, authorEntry, dateCreateLabel, dateCreatedEntry, descriptionLabel, descriptionEntry,\
        sourceLabel, sourceEntry
    global placeNameLabel, placeNameEntry, eventNameLabel, eventNameEntry

    saveButton.grid_forget()
    infoLabel.grid_forget()
    saveButton.grid_forget()
    personNameLabel.grid_forget()
    personNameEntry.grid_forget()
    authorLabel.grid_forget()
    authorEntry.grid_forget()
    dateCreateLabel.grid_forget()
    dateCreatedEntry.grid_forget()
    descriptionLabel.grid_forget()
    descriptionEntry.grid_forget()
    sourceLabel.grid_forget()
    sourceEntry.grid_forget()
    placeNameLabel.grid_forget()
    placeNameEntry.grid_forget()
    eventNameLabel.grid_forget()
    eventNameEntry.grid_forget()
    nameLabel = Label(root, text='\t\t')
    nameLabel.grid(row=3 + imgRowSpan - 1, column=1, columnspan=imgColSpan)

    counterLabel = Label(root, text='\t     ')
    counterLabel.grid(row=4 + imgRowSpan - 1, column=1, pady=(10, 0))


def importPhotos(tag):
    # path = filedialog.askdirectory()
    if tag:
        file_path = filedialog.askopenfiles()
    else:
        file_path = filedialog.askdirectory()
    # print(file_path)
    if file_path != '':
        reset()
        if tag:
            build_images_list(file_path, tag)
        else:
            build_images_list(file_path, tag)
            recognize()



def build_images_list(file_path, tag):
    global button_forward, paths, images, face_dict
    if tag:
        paths = [path.name for path in file_path]
    else:
        paths_jpg = glob.glob(file_path + '/*.jpg')
        paths_jpeg = glob.glob(file_path + '/*.jpeg')
        paths_png = glob.glob(file_path + '/*.png')
        paths = []
        for path_i in paths_jpg: paths.append(path_i)
        for path_i in paths_png: paths.append(path_i)
        for path_i in paths_jpeg: paths.append(path_i)
    for j in range(0,len(paths)):

        face_dic1,photo = get_faces(paths[j])
        # print(face_dic1)
        face_dict.append(face_dic1)
        photo = Image.fromarray(photo)
        photo = photo.resize((img_h, img_w), Image.ANTIALIAS)
        images.append(ImageTk.PhotoImage(photo))

    if len(paths) > 1:
        button_forward['state'] = NORMAL
    # print(len(images))
    build_photos_viewer(tag)





def build_photos_viewer(tag):
    print(paths[counter])
    global nameLabel, counterLabel,img,canvas

    img = Label(root, image=images[counter])
    img.photo = images[counter]
    img.grid(row=1, column=0, rowspan=imgRowSpan, columnspan=imgColSpan, padx=(20, 0))


    nameLabel = Label(root, text=paths[counter].split('/')[-1].split('.')[0])
    nameLabel.grid(row=3+imgRowSpan-1, column=0, columnspan=imgColSpan)

    counterLabel.config(text=f'Photo {counter+1} of {len(images)}')
    counterLabel.grid(row=4+imgRowSpan-1, column=1, pady=(10, 0))
    if tag:
        build_info_getter()



def build_info_getter():
    global saveButton, infoLabel, saveButton, personNameLabel, personNameEntry
    global authorLabel, authorEntry, dateCreateLabel, dateCreatedEntry, descriptionLabel, descriptionEntry,\
        sourceLabel, sourceEntry
    global placeNameLabel, placeNameEntry, eventNameLabel, eventNameEntry

    infoLabel.config(text = "Information for Metadata", font = 'Times 10 bold')
    infoLabel.grid(row=0, column=4, padx=(20, 0))

    personNameLabel.config(text='Name(s)  (name 1; name 2; ...)')
    personNameLabel.grid(row=1, column=4)
    personNameEntry.grid(row=2, column=4)

    authorLabel.config(text="Photographer")
    authorLabel.grid(row=3, column=4)
    authorEntry.grid(row=4, column=4)

    dateCreateLabel.config(text='Date  (YYYY-MM-DD)')
    dateCreateLabel.grid(row=5, column=4)
    # dateCreatedEntry.insert(0, 'Ex: 31/12/2021')
    dateCreatedEntry.grid(row=6, column=4)

    placeNameLabel.config(text='Place')
    placeNameLabel.grid(row=7, column=4)
    placeNameEntry.grid(row=8, column=4)

    eventNameLabel.config(text='Event')
    eventNameLabel.grid(row=9, column=4)
    eventNameEntry.grid(row=10, column=4)

    descriptionLabel.config(text='Description')
    descriptionLabel.grid(row=11, column=4)
    descriptionEntry.grid(row=12, column=4)

    sourceLabel.config(text='Source')
    sourceLabel.grid(row=13, column=4)
    sourceEntry.grid(row=14, column=4)

    saveButton.config(text= 'Save', command=lambda:save([],True))
    saveButton.grid(row=15, column=4)


    # personNameLabel = Label(root, text="Name")
    # personNameLabel.grid(row=1, column=3)


def create_metaData(metaDic,photograph_name):
    global  paths
    imageMeta_df = pd.DataFrame(metaDic, columns=metaDic.keys())

    general_filePath=re.findall(".*\/", paths[counter].replace("\\", "/"))[0]+"general_metaData.csv"
    print(general_filePath,paths[counter])

    try:
        general_df=pd.read_csv(general_filePath)
        general_df_len=len(general_df.loc[general_df["photograph_name"] == photograph_name])
        if general_df_len==0:
            frames = [general_df,imageMeta_df]
            result = pd.concat(frames, ignore_index=True)

            result.to_csv(general_filePath, columns=metaDic.keys())
        else:
            general_df.to_csv(general_filePath, columns=metaDic.keys())
    except:
        imageMeta_df.to_csv(general_filePath)
    imageMeta_filePath = re.findall(".*\/", paths[counter].replace("\\", "/"))[0]+"Meta_data/"+ paths[counter].replace("\\", "/").split("/")[-1].split(".")[0] + "_metaData.csv"
    print(imageMeta_filePath)

    imageMeta_df.to_csv(imageMeta_filePath)


def save(people,tagbool):
    global face_dict,paths
    global personNameEntry,authorEntry, dateCreatedEntry,placeNameEntry,eventNameEntry,descriptionEntry, sourceEntry
    if tagbool==False:
        person_var=people
    else:
        person_var = personNameEntry.get()
        person_var = person_var.split(";")
        print(person_var)
        for i in range(len(person_var)):
            person_var[i] = person_var[i].strip()

        if person_var[-1] == '':
            person_var = person_var[:-1]
        print(person_var)

    photograapher_var = authorEntry.get()
    date_var = dateCreatedEntry.get()
    place_var = placeNameEntry.get()
    event_var = eventNameEntry.get()
    desc_var = descriptionEntry.get()
    source_var = sourceEntry.get()





    photograph_name=paths[counter].replace("\\", "/").split("/")[-1]
    metadata={

        "photograph_name":[photograph_name],
        "persons":[person_var],
        "photographer":[photograapher_var],
        "date":[date_var],
        "place":[place_var],
        "event":[event_var],
        "description":[desc_var],
        "source":[source_var]
    }
    create_metaData(metadata,photograph_name)
    if tagbool==True:

        photo=tag(face_dict[counter], person_var,paths[counter])

        photo = Image.fromarray(photo)
        photo = photo.resize((img_h, img_w), Image.ANTIALIAS)
        images[counter]=ImageTk.PhotoImage(photo)
        build_photos_viewer(True)
    personNameEntry.delete(0,END)
    authorEntry.delete(0, END)
    dateCreatedEntry.delete(0, END)
    placeNameEntry.delete(0, END)
    eventNameEntry.delete(0, END)
    descriptionEntry.delete(0, END)
    sourceEntry.delete(0, END)


def recognize():
    global face_dict,counter
    image_counter=0
    people=[]
    for unknown_path in paths:
        unknown_path = unknown_path.replace('\\', '/')
        img_name = unknown_path.split('/')[-1]
        unkonwn_img = face_recognition.load_image_file(unknown_path)

        unkonwn_img_encodings = face_recognition.face_encodings(unkonwn_img)

        photo = paths[image_counter]
        photo = pre_processing(photo)

        i=0
        for unkonwn_img_encoding in unkonwn_img_encodings:
            knowns_path = re.findall(".*\/", paths[image_counter])[0]+"faces/training_set"
            knowns_paths = glob.glob(knowns_path+"/*")
            found_flag = False
            for path in knowns_paths:
                path = path.replace('\\', '/')
                encodings = read_encodings(path)
                # print("done reading encodings")
                check = face_recognition.compare_faces(encodings, unkonwn_img_encoding)
                # if check.count(True)/len(check) >= 0.8:

                if len(check) and check.count(True)/len(check) >= 0.8:
                    personDetectedName = path.split('/')[-1]
                    # print(f"person detected: {personDetectedName}")
                    people.append(personDetectedName)
                    photo = reco(face_dict[image_counter]["X" + str(i + 1)], personDetectedName, photo)

                    found_flag = True
                    break

            if not found_flag:

                # print(f"Could not match this face ({img_name}) to any person in our database")
                photo = reco(face_dict[image_counter]["X" + str(i + 1)], "X"+str(i + 1), photo)
                people.append("X"+str(i + 1))
            i += 1
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        photo = Image.fromarray(photo)
        photo = photo.resize((img_h, img_w), Image.ANTIALIAS)
        images[image_counter] = ImageTk.PhotoImage(photo)

        save(people,False)
        image_counter += 1
        counter = image_counter
        people=[]
    counter=0
    build_photos_viewer(False)


def go_forward():
    global img, images, counter
    if counter < len(images)-1:
        counter += 1

        img.grid_forget()
        img = Label(root, image=images[counter])
        img.photo = images[counter]
        img.grid(row=1, column=0, rowspan=imgRowSpan, columnspan=imgColSpan, padx=(20, 0))

        nameLabel.config(text=paths[counter].split('/')[-1].split('.')[0])
        counterLabel.config(text=f'Photo {counter+1} of {len(images)}')
        if counter == len(images)-1:
            global button_forward
            button_forward['state'] = DISABLED
    if counter > 0:
        global button_backward
        button_backward['state'] = NORMAL


def go_backward():
    global img, images, counter
    if counter > 0:
        counter -= 1
        img.grid_forget()
        img = Label(root, image=images[counter])
        img.photo = images[counter]
        img.grid(row=1, column=0, rowspan=imgRowSpan, columnspan=imgColSpan, padx=(20, 0))
        nameLabel.config(text=paths[counter].split('/')[-1].split('.')[0])
        counterLabel.config(text=f'Photo {counter+1} of {len(images)}')
        if counter == 0:
            global button_backward
            button_backward['state'] = DISABLED

    if counter < len(images) - 1:
        global button_forward
        button_forward['state'] = NORMAL


def build_environment():
    root_help = Tk()
    root_help.title('Help')
    root_help.geometry("420x270")

    create_env_label = Label(root_help, text='Click the button below to choose where to create the working environment')
    create_env_label.pack()
    # create_env_label.config()
    create_env_button = Button(root_help, text='Create Environment', bd=2, command=mkdirs, relief=GROOVE)

    # create_env_button.pack()
    # blog_label.pack()
    # contact_label.pack()
    # andrew_label.pack()
    # sherif_label.pack()

    blog_label = Label(root_help, text='Check our blog', fg="blue", cursor="hand2")
    blog_label.bind("<Button-1>", lambda e: callback("https://andrew-hany.github.io/Library_internship/"))

    contact_label = Label(root_help, text='Contact us:')

    andrew_label = Text(root_help,  height=1, borderwidth=0, width=36, bg='#F5F5F5')
    andrew_label.insert(1.0, 'Andrew Hany: andrewhany@aucegypt.edu')

    sherif_label = Text(root_help,  height=1, borderwidth=0, width=40, bg='#F5F5F5')
    sherif_label.insert(1.0, 'Sherif Sakran: sherifsakran@aucegypt.edu')

    create_env_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
    create_env_button.grid(row=1, column=1, pady=10, padx=10)
    blog_label.grid(row=2, column=1, pady=10, padx=10)
    contact_label.grid(row=3, column=1, pady=10, padx=10)

    andrew_label.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
    sherif_label.grid(row=5, column=0, columnspan=3, pady=10, padx=10)


def callback(url):
    webbrowser.open_new(url)


def mkdirs():
    path = filedialog.askdirectory()
    if path != '':
        try:
            environment = "Environment"
            os.mkdir(path+ "/" + environment)
            os.mkdir(path+ "/" + environment + "/faces")
            os.mkdir(path+ "/" + environment + "/faces" + "/training_set")
            os.mkdir(path+ "/" + environment + "/images")
            os.mkdir(path+ "/" + environment + "/images" + "/Meta_data")
        except FileExistsError:
            print('file already exists')


root = Tk()
root.title('Face Recognition')
root.geometry("570x500")
# p1 = PhotoImage(file='icon.png')
# root.iconphoto(False, p1)


explore_button = Button(root, text='Tag Faces', bd=2, command=lambda:importPhotos(True), relief=GROOVE)
explore_button.grid(row=0, column=0, pady=10, padx=(20, 0))

recognize_button = Button(root, text='Recognize Faces', bd=2, command=lambda:importPhotos(False), relief=GROOVE)
recognize_button.grid(row=0, column=2, pady=10)

canvas = Canvas(
    root,
    height=img_h,
    width=img_h,
    bg="#fff"
)
# canvas.pack()
canvas.grid(row=1, column=0, rowspan=imgRowSpan, columnspan=imgColSpan, padx=(20, 0))





img = Label(root)

button_backward = Button(root, text='Back', state=DISABLED, command=go_backward)
button_backward.grid(row=2+imgRowSpan-1, column=0, pady=5)

button_forward = Button(root, text='Next', state=DISABLED, command=go_forward)
button_forward.grid(row=2+imgRowSpan-1, column=2, pady=5)


nameLabel = Label(root, text='\t\t')
nameLabel.grid(row=3+imgRowSpan-1, column=1, columnspan=imgColSpan)

counterLabel = Label(root, text='\t     ')
counterLabel.grid(row=4+imgRowSpan-1, column=1, pady=(10, 0))

helpButton = Button(root, text='Help', command=build_environment)
helpButton.grid(row=5+imgRowSpan-1, column=1, pady=(10, 0))

emptyColumn = Label(root, text='\t')
emptyColumn.grid(row=0, column=3, rowspan=5+imgRowSpan)

# canvas2 = Canvas(
#     root,
#     height=img_h,
#     width=img_h * 0.5,
#     bg="#fff"
# )
# canvas2.grid(row=1, column=4)

infoLabel = Label(root)

personNameLabel = Label(root)

personNameEntry = Entry(root)

authorLabel = Label(root)
authorEntry = Entry(root)

dateCreateLabel = Label(root)
dateCreatedEntry = Entry(root)

placeNameLabel = Label(root)
placeNameEntry = Entry(root)

eventNameLabel = Label(root)
eventNameEntry = Entry(root)

descriptionLabel = Label(root)
descriptionEntry = Entry(root)

sourceLabel = Label(root)
sourceEntry = Entry(root)

saveButton = Button(root)


# rectangle=canvas.create_rectangle(
#         0 ,100 ,100, 20,
#         outline="#fb0",
#         fill="#fb0")

root.mainloop()