import face_recognition
import glob
import cv2

def build_encodings(path, n):
    person_path = path + "/*.jpg"
    person_photos_paths = glob.glob(person_path)
    min_imgs_numner = min(len(person_photos_paths), n)
    person_photos_paths = person_photos_paths[:min_imgs_numner]
    # print(person_photos_paths)

    person_images = []
    for path_i in person_photos_paths:
        person_images.append(face_recognition.load_image_file(path_i))
        # print(path_i)
    model_name = path.split("/")[-1]
    # print(model_name)
    with open(f"{path}/{model_name}_encodings.txt", 'w') as f:
        print("Starting encodings")
        person_images_encodings = []
        for img in person_images:
            person_images_encodings.append(face_recognition.face_encodings(img)[0])
            # print(face_recognition.face_encodings(img)[0])
            f.write(str(face_recognition.face_encodings(img)[0]))
            f.write("\n\n")
            
            
def read_encodings(path):
    file_name = path + '/' + path.split('/')[-1]+"_encodings.txt"
    encodings = []
    # print(file_name)
    with open(file_name) as f:
        content = f.read()
        encodings_read = content.split("\n\n")
        encodings_read = encodings_read[0:-1]
        for encoding_read in encodings_read:
            encoding_read = encoding_read[1:-1]
            temp = encoding_read.split()
            floats = [float(x) for x in temp]
            encodings.append(floats)
    return encodings


def recognize_faces(unkowns_path):
    unknowns_paths = glob.glob(unkowns_path+"/*.jpg")
    for unknown_path in unknowns_paths:
        unknown_path = unknown_path.replace('\\', '/')
        img_name = unknown_path.split('/')[-1]
        unkonwn_img = face_recognition.load_image_file(unknown_path)
        unkonwn_img_encoding = face_recognition.face_encodings(unkonwn_img)[0]
        knowns_path = "C:/Users/data/PycharmProjects/pythonProject/faces/training_set"
        knowns_paths = glob.glob(knowns_path+"/*")
        found_flag = False
        for path in knowns_paths:
            path = path.replace('\\', '/')
            encodings = read_encodings(path)
            print("done reading encodings")
            check = face_recognition.compare_faces(encodings, unkonwn_img_encoding)
            print("done comparing")
            if check.count(True) >= 4: #not accurate (if it matches two images for dalal and two encodings of another person
                img = cv2.imread(unknown_path, 1)
                cv2.imshow(f"person detected: {path.split('/')[-1]}", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # print(f"This face ({img_name}) belongs to: {path.split('/')[-1]}")
                found_flag = True
                break
        if not found_flag:
            print(f"Could not match this face ({img_name}) to any person in our database")