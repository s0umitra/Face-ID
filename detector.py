"""
Environment
python : 3.5
cuda : 10.1
Motivation : https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

"""

import face_recognition
import pickle
import cv2
import os
from resizer import ori_in

# r=root, d=directories, f=files
files = []
for r, d, f in os.walk('database'):
    for file in f:
        if '.jpg' or '.jpeg' or '.png' in file:
            files.append(os.path.join(r, file))

face_details = []
names = []

print("Encoding Faces...")

for (i, file_name) in enumerate(files):

    # extract the person name from the image path
    print("Reading Face : {}/{}".format(i + 1, len(files)) + " : " + str(file_name.split('\\')[2]))
    name = file_name.split('\\')[1]

    # resizing image
    org_img = cv2.imread(file_name)
    image = ori_in(org_img)

    # converting image to from BGR to RGB
    iRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(iRGB, model='cnn')
    details = face_recognition.face_encodings(iRGB, locations, num_jitters=100)

    for n in details:
        face_details.append(n)
        names.append(name)

# saving face details to a file
face_dump = {"details": face_details, "names": names}
f = open('data.sys', "wb")
f.write(pickle.dumps(face_dump))
f.close()

print("All available faces are encoded and saved to : data.sys")
