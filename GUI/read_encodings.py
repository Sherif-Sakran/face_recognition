import face_recognition
import glob

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