import face_recognition
from read_encodings import read_encodings
import glob
import re
import time
from multiprocessing import Process
import PIL

def recognize(path, knowns_path):
    image_counter = 0
    people = []
    paths = glob.glob(path + "/*")
    knowns_paths = glob.glob(knowns_path + "/*")

    processes = []
    for unknown_path in paths:
        process = Process(target=recogize_each, args=(unknown_path, knowns_paths, ))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def recogize_each(unknown_path, knowns_paths ):
    unknown_path = unknown_path.replace('\\', '/')
    img_name = unknown_path.split('/')[-1]
    print(f'img: {img_name}')
    try:
        unknown_img = face_recognition.load_image_file(unknown_path)
    except PIL.UnidentifiedImageError:
        return
    except PermissionError:
        return
    # print(unknown_img)

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
                print(f"person detected: {personDetectedName}")
                found_flag = True
                break

        if not found_flag:
            print(f"Could not match this face to any person in our database")
    print('')


if __name__ == "__main__":
    unkowns_path = "D:\Courses\9- Summer 2022\Internship\Library_internship-main\Environment\images"
    knowns_path = "D:\\Courses\\9- Summer 2022\\Internship\\Library_internship-main\\Environment\\faces\\training_set"
    time1 = time.time()
    recognize(unkowns_path, knowns_path)
    print(f'time taken: {time.time() - time1}')


