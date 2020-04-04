import os
import random
import face_recognition
import pickle
import cv2
from resizer import ori_in

f = open("config.cfg", "r")
configs = f.read()
lines = f.readlines()
for x in configs:
    if x == "method":
        configs.split()
        method = str(configs[:])

data = pickle.loads(open('data.sys', "rb").read())
count = 0
files = []

# r=root, d=directories, f=files
for r, d, f in os.walk('input'):
    for file in f:
        if '.jpg' or '.jpeg' or '.png' in file:
            files.append(os.path.join(r, file))


def recognizer(file_name):
    print("Working on : " + str(file_name.split('\\')[1]))

    # resizing image (1200 x 1200)
    org_img = cv2.imread(file_name)
    image = ori_in(org_img)

    # converting image from BGR to RGB
    iRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # image is scaled up for better processing
    locations = face_recognition.face_locations(iRGB, model='cnn')
    details = face_recognition.face_encodings(iRGB, locations, num_jitters=100)

    names = []
    names_known = []

    for k in details:
        matches = face_recognition.compare_faces(data["details"], k, tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:

            matches = [k for (k, b) in enumerate(matches) if b]
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
    fn = "Output_" + str(count + 1) + "_" + ns + ".jpg"
    cv2.imwrite(("output/" + fn), image)
    cv2.waitKey(0)
    print("Saved output to : " + fn)


for (i, file) in enumerate(files):
    recognizer(file)

print("----Done----")
