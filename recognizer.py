import os
import random
import face_recognition
import pickle
import cv2

from resizer import ori_in

data = pickle.loads(open('data.sys', "rb").read())
count = 0
files = []

# r=root, d=directories, f=files
for r, d, f in os.walk('input'):
    for file in f:
        if '.jpg' or '.jpeg' or '.png' in file:
            files.append(os.path.join(r, file))

for (i, file_name) in enumerate(files):

    print("Working on : " + str(file_name.split('\\')[1]))

    # resizing image
    org_img = cv2.imread(file_name)
    image = ori_in(org_img)

    # converting image to from BGR to RGB
    iRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(iRGB, number_of_times_to_upsample=2, model='cnn')
    details = face_recognition.face_encodings(iRGB, locations, num_jitters=100)

    # initialize the list of names for each face detected
    names = []
    names_known = []

    # loop over the facial embeddings
    for i in details:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["details"], i, tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matches = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matches:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
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

print("----Done----")
