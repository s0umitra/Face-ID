import os
import cv2
import face_recognition
from resizer import ori_in

# r=root, d=directories, f=files
files = []
count = 0

for r, d, f in os.walk('face-cropper\\input'):
    for file in f:
        if '.jpg' or '.jpeg' or '.png' in file:
            files.append(os.path.join(r, file))

for (i, file_name) in enumerate(files):
    print("Working on : " + str(file_name.split('\\')[2]))

    org_img = cv2.imread(file_name)
    image = ori_in(org_img)

    iRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(iRGB, model='cnn')

    for ((top, right, bottom, left), n) in zip(locations, range(0, len(locations))):
        # (x1,y1) as the top-left vertex and (x2,y2) as the bottom-right roi = im[y1:y2, x1:x2]
        img = image[top - 30:bottom + 30, left - 30:right + 30]
        cv2.imwrite('face-cropper\\output\\face_' + str(n + 1) + "_.jpg", img)

    print("Faces found : " + str(len(locations)))
    print("Cropped Faces to output folder of face-cropper.")