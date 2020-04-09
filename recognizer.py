import os
import random
import face_recognition
import pickle
import cv2

from arguments import arguments
from resizer import ori_in


def boot():
    mode, scale, e_res, r_res, jitts = arguments()
    print("Configurations :-\n\tModel = {}\n\tUpscale-factor = {}\n\tDetector's Image Resolution = {}\n\tRecognizer's "
          "Image Resolution = {}\n\tJitters = {} ".format(mode, scale, e_res, r_res, jitts))


def file_crawler(base):
    files = []
    for r, d, f in os.walk(base):
        for one_file in f:
            if '.jpg' or '.jpeg' or '.png' in one_file:
                files.append(os.path.join(r, one_file))

    return files


def loader(name, res, scale, mode, jitts):
    org_img = cv2.imread(name)
    image = ori_in(org_img, int(res))
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(img_RGB, number_of_times_to_upsample=int(scale), model=mode)
    details = face_recognition.face_encodings(img_RGB, locations, num_jitters=int(jitts))

    return image, locations, details


def recognizer(file_name):
    data = pickle.loads(open('data.sys', "rb").read())
    names = []
    names_known = []

    mode, scale, e_res, r_res, jitts = arguments()
    image, locations, details = loader(file_name, r_res, scale, mode, jitts)

    for y in details:
        matches = face_recognition.compare_faces(data["details"], y, tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:

            for (ID, value) in enumerate(matches):
                if value:
                    matches = [ID]

            counts = {}

            for k in matches:
                name = data["names"][k]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            names_known.append(name)

        # update the list of names
        names.append(name)

    return locations, names_known, names, image


def line_draw(image, left_top, right_bottom, color, thickness):
    # left_top = (left, top)
    # right_bottom = (right, bottom)

    # dash's length
    per = int(abs(left_top[0] - right_bottom[0]) * (20 / 100))

    # top line
    start_point = [left_top, (right_bottom[0], left_top[1])]
    end_point = [(left_top[0] + per, left_top[1]), (right_bottom[0] - per, left_top[1])]
    for x, y in zip(start_point, end_point):
        cv2.line(image, x, y, color, thickness)

    # bottom line
    start_point = [(left_top[0], right_bottom[1]), right_bottom]
    end_point = [(left_top[0] + per, right_bottom[1]), (right_bottom[0] - per, right_bottom[1])]
    for x, y in zip(start_point, end_point):
        cv2.line(image, x, y, color, thickness)

    # left line
    start_point = [left_top, (left_top[0], right_bottom[1])]
    end_point = [(left_top[0], left_top[1] + per), (left_top[0], right_bottom[1] - per)]
    for x, y in zip(start_point, end_point):
        cv2.line(image, x, y, color, thickness)

    # right line
    start_point = [(right_bottom[0], left_top[1]), right_bottom]
    end_point = [(right_bottom[0], left_top[1] + per), (right_bottom[0], right_bottom[1] - per)]
    for x, y in zip(start_point, end_point):
        cv2.line(image, x, y, color, thickness)


def box_draw(q, rec):
    # loop over the recognized faces
    locations, names_known, names, image = rec

    for ((top, right, bottom, left), name) in zip(locations, names):
        # draw the predicted face name on the image
        R = random.choice(range(0, 240, 20))
        G = random.choice(range(0, 240, 20))
        B = random.choice(range(0, 240, 20))
        RGB = (R, G, B)

        # draw lines over the face
        # cv2.rectangle(image, (left, top), (right, bottom), (R, G, B), 2)
        x = (left, top)
        y = (right, bottom)
        line_draw(image, x, y, (R, G, B), 2)
        
        # draw name
        cv2.putText(image, name, (left, top - 10 if top > 15 else bottom + 10), cv2.FONT_HERSHEY_DUPLEX, .60, (R, G, B), 2)
        
    # Save the output image
    ns = '_'.join([str(n) for n in names_known])
    fn = "Output_" + str(q + 1) + "_" + ns + ".jpg"
    cv2.imwrite(("output/" + fn), image)
    print("Saved output to : " + fn)


if __name__ == "__main__":

    boot()
    file_list = file_crawler("input")

    for (i, file) in enumerate(file_list):
        print("Working on : " + str(file.split('\\')[1]))
        box_draw(i, recognizer(file))

    print("----Done----")
