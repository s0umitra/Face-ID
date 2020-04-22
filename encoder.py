"""
Environment:-
python : 3.5
cuda : 10.1
cnn method - it would be advised to run cnn method on cuda enabled environment with gpu ( >= 4gb vram)

"""


import pickle

from main_lib import boot_loader, file_crawler, image_frame_loader


def encoder(file_name):
    faces = []
    names = []

    for (i, file) in enumerate(file_name):

        name = file.split('\\')[-2]
        print("Reading Face : {}/{}".format(i + 1, len(file_name)) + " : {} : {}".format(str(file.split('\\')[-2]),
                                                                                         str(file.split('\\')[-1])))

        image, face_locations, face_details = image_frame_loader(file, args, 'encoder')

        for n in face_details:
            faces.append(n)
            names.append(name)

        data = {"details": faces, "names": names}
        f = open('data.sys', "wb")
        f.write(pickle.dumps(data))
        f.close()


if __name__ == "__main__":
    args = boot_loader('encoder', 'encoder')
    file_list = file_crawler("database")

    print("\nEncoding Faces..", flush=True)
    encoder(file_list)
    print("\nAll available faces are encoded and saved to : data.sys")
