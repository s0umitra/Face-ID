import os
import cv2

from main_lib import boot_loader, image_frame_loader, recognizer, file_crawler, dataset_loader


def face_cropper(files):
    count = 0
    root = 'data-builder\\'
    temp_file = root + 'temp.jpg'

    for (i, file_name) in enumerate(files):

        index = 0
        kn = 0
        uk = 0

        print("\nProcessing    : ", file_name.split('\\')[-1])

        image, face_locations, face_details = image_frame_loader(file_name, args, 'set-builder')
        print("Faces found   : ", len(face_locations))

        names = recognizer(face_details, dataset, args[4])

        for ((top, right, bottom, left), n) in zip(face_locations, range(0, len(face_locations))):

            Done = False
            padding = 30

            while not Done:
                img = image[top - padding:bottom + padding, left - padding:right + padding]
                try:
                    cv2.imwrite(temp_file, img)
                    Done = True
                except:
                    padding -= 5

            if names[n] == "Unknown":
                path = os.path.join(root, 'output\\_Unknowns_\\')
                uk += 1
            else:
                path = os.path.join(root, 'output\\' + str(names[n])) + '\\'
                kn += 1

            if not os.path.exists(path):
                os.mkdir(path)

            try:
                os.rename(root + 'temp.jpg', path + str(i) + str(n) + str(index) + '.jpg')
            except FileExistsError:
                index += 1
                pass

        print("Known Faces   : ", kn)
        print("Unknown Faces : ", uk)
        count += len(face_locations)

    print("\nTotal faces cropped : ", count)


if __name__ == "__main__":

    file_list = file_crawler('data-builder\\src')
    args = boot_loader('set-builder', 'set-builder')
"""
    dataset = dataset_loader()
    face_cropper(file_list)"""
