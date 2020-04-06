"""
Environment:-
python : 3.5
cuda : 10.1
cnn method - it would be advised to run cnn method on cuda enabled environment with gpu ( >= 4gb vram)

"""

import pickle
from recognizer import loader, boot, file_crawler
from arguments import arguments


def decoder(file_name):

    face_details = []
    names = []

    for (i, files) in enumerate(file_name):
        print("Reading Face : {}/{}".format(i + 1, len(file_name)) + " : " + str(files.split('\\')[-1]))
        name = files.split('\\')[1]

        mode, scale, e_res, r_res, jitts = arguments()
        image, locations, details = loader(files, e_res, scale, mode, jitts)

        for n in details:
            face_details.append(n)
            names.append(name)

    return face_details, names


def dumper(face_details, names):
    # saving face details to a file
    face_dump = {"details": face_details, "names": names}
    f = open('data.sys', "wb")
    f.write(pickle.dumps(face_dump))
    f.close()


if __name__ == "__main__":

    boot()
    file_list = file_crawler("database")
    print("Encoding Faces..", flush=True)

    faces, f_names = decoder(file_list)
    dumper(faces, f_names)

    print("\nAll available faces are encoded and saved to : data.sys")
