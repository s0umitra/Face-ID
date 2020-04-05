"""
Environment:-
python : 3.5
cuda : 10.1
uses cnn method - it would be good only to run it in cuda enabled environment with gpu( >= 4gb vram)

"""

import pickle
from recognizer import loader, boot, file_crawler
from arguments import arguments


def decoder(file_name):
    print("Reading Face : {}/{}".format(i + 1, len(file_list)) + " : " + str(file_name.split('\\')[-1]))
    name = file_name.split('\\')[1]

    mode, scale, e_res, r_res, jitts = arguments()
    image, locations, details = loader(file_name, e_res, scale, mode, jitts)

    for n in details:
        face_details.append(n)
        names.append(name)


if __name__ == "__main__":
    file_list = file_crawler("database")
    face_details = []
    names = []

    boot()
    print("Encoding Faces..", flush=True)

    for (i, files) in enumerate(file_list):
        decoder(files)

    # saving face details to a file
    face_dump = {"details": face_details, "names": names}
    f = open('data.sys', "wb")
    f.write(pickle.dumps(face_dump))
    f.close()

    print("\nAll available faces are encoded and saved to : data.sys")
