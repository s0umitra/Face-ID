import os
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN


def draw_faces(filename, result_list):
    # load the image
    data = pyplot.imread(filename)
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.savefig(os.getcwd() + '\\output\\' + 'image_' + str(n+1) + '_face_' + str(i+1) + '.jpg')


faces_path = os.getcwd() + '\\faces'
detector = MTCNN(min_face_size=80, scale_factor=0.6)

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(faces_path):
    for file in f:
        if '.jpg' in file:
            files.append(os.path.join(r, file))

for n in range(0, len(files)):
    filename = files[n]
    print(filename)
    # load image from file
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    # detect faces in the image
    faces = detector.detect_faces(pixels)
    # display faces on the original image
    draw_faces(filename, faces)


