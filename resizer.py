import cv2


# it you want to change resolution then change value 1200 to required one
def ori_in(org_img):
    (h, w) = org_img.shape[:2]
    if h > w and h > 2000:
        return image_resize(org_img, None, 2000)
    elif w > h and w > 2000:
        return image_resize(org_img, 2000, None)
    else:
        return org_img


# image resizing function
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    h, w = image.shape[:2]
    if width is None:
        # calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized
