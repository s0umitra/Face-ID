import os
import cv2

from face_lib import arguments, loader, recognizer, file_crawler


def face_cropper(files):
    count = 0
    root = 'data-builder\\'
    mode, scale, e_res, r_res, jitts = arguments()

    for (i, file_name) in enumerate(files):
        index = 0
        print("Working on : " + str(file_name.split('\\')[-1]))

        image, locations, details = loader(file_name, e_res, scale, mode, jitts)
        print("Faces found : " + str(len(locations)))

        for ((top, right, bottom, left), n) in zip(locations, range(0, len(locations))):

            img = image[top - 30:bottom + 30, left - 30:right + 30]

            cv2.imwrite(root + 'temp.jpg', img)

            locations, names_known, names, images = recognizer(root + 'temp.jpg')
            # print(locations, names_known, names)
            print('Face : ' + str(n + 1) + " : ", names)

            if names[0] == "Unknown":
                path = os.path.join(root, 'output\\_Unknowns_\\')
            else:
                path = os.path.join(root, 'output\\' + str(names_known[0])) + '\\'

            if not os.path.exists(path):
                os.mkdir(path)

            try:
                os.rename(root + 'temp.jpg', path + str(i) + str(n) + str(index) + '.jpg')
            except FileExistsError:
                index += 1
                pass

            count += len(locations)

    print("Total faces cropped : " + str(count))


if __name__ == "__main__":

    file_list = file_crawler('data-builder\\src')
    face_cropper(file_list)
