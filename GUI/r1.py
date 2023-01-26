import face_recognition
from read_encodings import read_encodings
import glob
import re
import time
import PIL


def recognition_model_driver(path):
    # recognition model is to be set here to direct to a specific directory
    knowns_path = "D:\\Courses\\9- Summer 2022\\Internship\\Library_internship-main\\Environment\\faces\\training_set"
    recognize(path, knowns_path)


def recognize(path, knowns_path):
    paths = glob.glob(path + "/*")
    knowns_paths = glob.glob(knowns_path + "/*")

    for unknown_path in paths:
        unknown_path = unknown_path.replace('\\', '/')
        img_name = unknown_path.split('/')[-1]
        # print(f'img: {img_name}')
        try:
            unknown_img = face_recognition.load_image_file(unknown_path)
        except PIL.UnidentifiedImageError:
            continue
        except PermissionError:
            continue

        unknown_img_encodings = face_recognition.face_encodings(unknown_img)

        for unknown_img_encoding in unknown_img_encodings:
            found_flag = False
            for path in knowns_paths:
                path = path.replace('\\', '/')
                encodings = read_encodings(path)
                # print("done reading encodings")
                check = face_recognition.compare_faces(encodings, unknown_img_encoding)
                # if check.count(True)/len(check) >= 0.8:

                if len(check) and check.count(True) / len(check) >= 0.8:
                    personDetectedName = path.split('/')[-1]
                    print(f"img: {img_name}, person detected: {personDetectedName}")
                    found_flag = True
                    break

            if not found_flag:
                print(f"img: {img_name}, person detected: unknown")
        print('')


if __name__ == "__main__":
    unknowns_path = "D:\Courses\9- Summer 2022\Internship\Library_internship-main\Environment\images"
    knowns_path = "D:\\Courses\\9- Summer 2022\\Internship\\Library_internship-main\\Environment\\faces\\training_set"
    time1 = time.time()
    recognize(unknowns_path, knowns_path)
    print(f'time taken: {time.time() - time1}')