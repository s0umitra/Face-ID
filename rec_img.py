from main_lib import boot_loader, image_frame_loader, recognizer
from main_lib import draw_box, dataset_loader, file_crawler, save_output_image

if __name__ == "__main__":
    # Load the configurations from the config file
    args = boot_loader('rec-img', 'rec-img')

    dataset = dataset_loader()
    file_list = file_crawler("input\\image")

    print("\nFound {} Images to process!".format(len(file_list)))

    for (i, file) in enumerate(file_list):
        print("\nProcessing {}/{} : ".format(i + 1, len(file_list)) + file.split('\\')[-1])

        image, face_locations, face_details = image_frame_loader(file, args, 'rec-img')
        names = recognizer(face_details, dataset, args[4])
        final_image = draw_box(1, image, names, face_locations)
        save_output_image(i, names, final_image)

    print("\n------Task Completed------")
