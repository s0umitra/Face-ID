import os
import random
import face_recognition
import pickle
import cv2
from arguments import arguments
from resizer import ori_in


def boot():
    mode, scale, e_res, r_res, jitts = arguments()
    print("Configuration :-\n\tModel = {}\n\tUpscale-factor = {}\n\tDetector's Image Resolution = {}\n\tRecognizer's "
          "Image Resolution = {}\n\tJitters = {} ".format(mode, scale, e_res, r_res, jitts))


def file_crawler(base):
    files = []
    for r, d, f in os.walk(base):
        for file in f:
            if '.jpg' or '.jpeg' or '.png' in file:
                files.append(os.path.join(r, file))
    return files


def loader(name, res, scale, mode, jitts):
    org_img = cv2.imread(name)
    image = ori_in(org_img, int(res))
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(img_RGB, number_of_times_to_upsample=int(scale), model=mode)
    details = face_recognition.face_encodings(img_RGB, locations, num_jitters=int(jitts))

    return image, locations, details


def recognizer(q, file_name):
    print("Working on : " + str(file_name.split('\\')[1]))

    mode, scale, e_res, r_res, jitts = arguments()

    image, locations, details = loader(file_name, r_res, scale, mode, jitts)

    data = pickle.loads(open('data.sys', "rb").read())
    names = []
    names_known = []

    for y in details:
        matches = face_recognition.compare_faces(data["details"], y, tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:

            matches = [y for (y, b) in enumerate(matches) if b]
            counts = {}

            for k in matches:
                name = data["names"][k]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            names_known.append(name)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(locations, names):
        # draw the predicted face name on the image
        R = random.choice(range(0, 255, 30))
        G = random.choice(range(0, 255, 30))
        B = random.choice(range(0, 255, 30))
        cv2.rectangle(image, (left, top), (right, bottom), (R, G, B), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (R, G, B), 2)

    # Save the output image
    ns = '_'.join([str(n) for n in names_known])
    fn = "Output_" + str(q + 1) + "_" + ns + ".jpg"
    cv2.imwrite(("output/" + fn), image)
    print("Saved output to : " + fn)


def main():
    print("Encoded faces loaded successfully")

    file_list = file_crawler("input")

    for (i, file) in enumerate(file_list):
        recognizer(i, file)

    print("----Done----")


if __name__ == "__main__":
    boot()
    main()
