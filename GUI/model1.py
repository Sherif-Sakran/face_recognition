import face_recognition
import glob
import cv2

def build_encodings(path, n):
    person_path = path + "/*.jpg"
    person_photos_paths = glob.glob(person_path)
    min_imgs_numner = min(len(person_photos_paths), n)
    person_photos_paths = person_photos_paths[:min_imgs_numner]
    # print(person_photos_paths)
    print(f'path: {path}')
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
            try:
                person_images_encodings.append(face_recognition.face_encodings(img)[0])
                f.write(str(face_recognition.face_encodings(img)[0]))
                f.write("\n\n")
            except IndexError:
                print('could not detect faces in this photo')
            # print(face_recognition.face_encodings(img)[0])

            
    print(f'done: {path}')
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