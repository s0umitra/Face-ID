import cv2

from main_lib import file_crawler, dataset_loader, boot_loader, image_frame_loader, recognizer, draw_box


def get_length(vid):
    vid.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    length = vid.get(cv2.CAP_PROP_POS_FRAMES)
    vid.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
    return length


def rec_vid(no, length, writer, args):

    file_name = None

    for q in range(0, int(length)):
        (return_value, frame) = stream.read()
        if not return_value:
            break

        image, face_locations, face_details = image_frame_loader(frame, args, 'rec-vid')
        names = recognizer(face_details, dataset, args[4])
        frame = draw_box(0, image, names, face_locations)

        file_path = "output/video/"
        file_name = "Output_" + str(no) + "_" + ".avi"
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

    if file_name is not None:
        print("Output saved to :", file_name)


if __name__ == '__main__':

    args = boot_loader('rec-vid-liv', 'rec-vid')
    dataset = dataset_loader()
    file_list = file_crawler("input\\video")
    print("\nPress 'z' to break execution!")

    for (i, file) in enumerate(file_list):
        print("\nProcessing {}/{} : ".format(i + 1, len(file_list)) + file.split('\\')[-1])
        
        stream = cv2.VideoCapture(file)
        length = get_length(stream)
        print("Totals frames : " + str(length))
        writer = None

        rec_vid(i, length, writer, args)

        stream.release()
        if writer is not None:
            writer.release()

    print("\n------Task Completed------")
