import sys

import cv2
from main_lib import dataset_loader, image_frame_loader
from main_lib import recognizer, draw_box, boot_loader


def rec_liv(args):
    writer = None
    ON = True
    while ON:
        (return_value, frame) = stream.read()

        image, face_locations, face_details = image_frame_loader(frame, args, 'rec-vid')
        names = recognizer(face_details, dataset, args[4])
        frame = draw_box(0, image, names, face_locations)

        if args[5] == '1':

            file_path = "output/video/"
            file_name = "Live_Output_.avi"
            file = file_path + file_name

            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(file, fourcc, 25,
                                         (frame.shape[1], frame.shape[0]), True)

            if writer is not None:
                writer.write(frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == ord('z'):
            break


if __name__ == '__main__':
    args = boot_loader('rec-vid-liv', 'rec-live')
    dataset = dataset_loader()
    print("\nPress 'z' to break execution! (Select Frame)")

    stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    rec_liv(args)

    stream.release()
    cv2.destroyAllWindows()
    print("\n------Task Completed------")
