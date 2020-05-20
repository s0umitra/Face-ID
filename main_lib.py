import os
import pickle
import random
import sys

import cv2
import face_recognition


def configs(use_type):
    path = os.getcwd()
    f = open(path + "\\config.cfg", "r")
    config_lines = f.readlines()

    conf_mode = ''
    command = ''
    value = ''
    error_flag = 0

    conf_detector = ['hog', '1', '1000', '100']
    conf_rec_img = ['hog', '1', '1500', '100', '0.4']
    conf_rec_vid_and_liv = ['hog', '1', '500', '0', '0.4', '0']

    for (i, line) in enumerate(config_lines):

        try:
            if config_lines[i][0] not in ('#', ' ', '\n'):

                if line.startswith('!'):
                    conf_mode = line.split()[1]

                if line.startswith('$'):
                    command = line.split('=')[0].split()[1]
                    value = line.split('=')[1].split()[0]

                if conf_mode == 'ENCODER':
                    if line.startswith('$'):

                        try:
                            if command == 'method' and value in ("hog", "cnn"):
                                conf_detector[0] = value
                            if command == 'upscale_factor' and int(value) <= 5:
                                conf_detector[1] = value
                            if command == 'encode_face_res' and int(value) <= 4000:
                                conf_detector[2] = value
                            if command == 'jitters' and int(value) <= 300:
                                conf_detector[3] = value
                        except:
                            error_flag = 1

                elif conf_mode == 'RECOGNIZE-IMG':
                    if line.startswith('$'):
                        try:
                            if command == 'method' and value in ("hog", "cnn"):
                                conf_rec_img[0] = value
                            if command == 'upscale_factor' and int(value) <= 5:
                                conf_rec_img[1] = value
                            if command == 'rec_img_resize' and int(value) <= 4000:
                                conf_rec_img[2] = value
                            if command == 'jitters' and int(value) <= 300:
                                conf_rec_img[3] = value
                            if command == 'tolerance' and float(value) <= 1:
                                conf_rec_img[4] = value
                        except:
                            error_flag = 1

                elif conf_mode == 'RECOGNIZE-VID-AND-LIV':
                    if line.startswith('$'):
                        try:
                            if command == 'method' and value in ("hog", "cnn"):
                                conf_rec_vid_and_liv[0] = value
                            if command == 'upscale_factor' and int(value) <= 5:
                                conf_rec_vid_and_liv[1] = value
                            if command == 'rec_vid_resize' and int(value) <= 2500:
                                conf_rec_vid_and_liv[2] = value
                            if command == 'jitters' and int(value) <= 300:
                                conf_rec_vid_and_liv[3] = value
                            if command == 'tolerance' and float(value) <= 1:
                                conf_rec_vid_and_liv[4] = value
                            if command == 'live_save_output' and int(value) in (0, 1):
                                conf_rec_vid_and_liv[5] = value
                        except:
                            error_flag = 1

        except:
            print("\nError detected in config.cfg")

    if error_flag == 1:
        print("Error in " + conf_mode + " configs, values set to default")
    if use_type == 'encoder':
        return conf_detector
    if use_type in ('rec-img', 'set-builder'):
        return conf_rec_img
    if use_type == 'rec-vid-liv':
        return conf_rec_vid_and_liv


def boot_loader(use_type, caller):
    arguments = configs(use_type)
    s = ''
    if use_type == 'encoder':
        mode = "Encoder's"
    else:
        mode = "Recognizer's"
        s = s + "\n\t{:20s}  ---> ".format('Tolerance') + arguments[4]
        if caller == 'rec-live':
            s = s + "\n\t{:20s}  ---> ".format('Save to Disk') + arguments[5]

    # print('{:32s} ---> {}'.format(prt_str[i], prt_out[i]))
    print(mode +
          " Configurations :-"
          "\n\t{:20s}  ---> ".format('Mode') + arguments[0] +
          "\n\t{:20s}  ---> ".format('Upscale-factor') + arguments[1] +
          "\n\t{:20s}  ---> ".format(mode) + arguments[2] +
          "\n\t{:20s}  ---> ".format('Jitters') + arguments[3] +
          s
          )
    return arguments


def image_frame_loader(frame, args, use_type):
    mode = args[0]
    up_scale = args[1]
    max_res = args[2]
    jitts = args[3]

    if use_type in ('rec-img', 'encoder', 'set-builder'):
        org_img = cv2.imread(frame)
    else:
        org_img = frame

    image = frame_optimizer(org_img, int(max_res))

    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img_RGB,
                                                     number_of_times_to_upsample=int(up_scale),
                                                     model=mode)
    face_details = face_recognition.face_encodings(img_RGB,
                                                   face_locations,
                                                   num_jitters=int(jitts))
    return image, face_locations, face_details


def dataset_loader():
    path = os.getcwd()
    if os.path.exists(path + '\\data.sys'):
        data = pickle.loads(open('data.sys', "rb").read())
        return data
    else:
        print("\nNo Encoded Data found!\n\nExiting!!!")
        sys.exit()


def recognizer(face_details, dataset, tol):
    names = []
    names_known = []

    for y in face_details:
        matches = face_recognition.compare_faces(dataset["details"], y, tolerance=float(tol))
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:

            for (ID, value) in enumerate(matches):
                if value:
                    matches = [ID]

            counts = {}

            for k in matches:
                name = dataset["names"][k]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            names_known.append(name)

        # update the list of names
        names.append(name)

    return names


def draw_box(RGB_factor, image, names, face_locations):
    for ((top, right, bottom, left), name) in zip(face_locations, names):
        if RGB_factor == 1:
            R = random.choice(range(0, 240, 20))
            G = random.choice(range(0, 240, 20))
            B = random.choice(range(0, 240, 20))
            RGB = (R, G, B)
        else:
            RGB = (0, 0, 255)
        x = (left, top)
        y = (right, bottom)
        line_draw(image, x, y, RGB, 2)
        cv2.putText(image, name,
                    (left, top - 10 if top > 15 else bottom + 20),
                    cv2.FONT_HERSHEY_DUPLEX, .60, RGB, 2)
    return image


def save_output_image(q, names, image):
    exist = 0

    known_names = '_'.join([str(n) for n in names if n != 'Unknown'])
    file_path = "output/image/"

    file_name = "Output_" + str(q + 1) + "_" + known_names + ".jpg"
    file = file_path + file_name

    while os.path.exists(file_path + file_name):
        file_name = "Output_" + str(q + 1) + "_" + known_names + "_" + str(exist) + ".jpg"
    exist += 1

    cv2.imwrite(file, image)
    print("Output saved to : " + file_name)


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


def frame_optimizer(org_img, scale):
    (height, width) = org_img.shape[:2]
    if height > scale or width > scale:
        if height > width:
            ratio = scale / float(height)
            new_res = (int(width * ratio), scale)
        elif width > height:
            ratio = scale / float(width)
            new_res = (scale, int(height * ratio))
        resized_img = cv2.resize(org_img, new_res, interpolation=cv2.INTER_AREA)
        return resized_img
    else:
        return org_img


def file_crawler(base):
    files = []
    for r, d, f in os.walk(base):
        for one_file in f:
            files.append(os.path.join(r, one_file))

    return files
