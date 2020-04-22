import cv2
from main_lib import dataset_loader, image_frame_loader
from main_lib import recognizer, draw_box, boot_loader


def rec_liv(args):
    while True:
        (return_value, frame) = stream.read()

        image, face_locations, face_details = image_frame_loader(frame, args, 'rec-vid')
        names = recognizer(face_details, dataset, args[4])
        frame = draw_box(0, image, names, face_locations)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('z'):
            break
    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = boot_loader('rec-vid-liv', 'rec-live')
    dataset = dataset_loader()

    stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    rec_liv(args)

    stream.release()

    print("\n------Task Completed------")
