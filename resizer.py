import cv2


# if you want to change resolution then change value scale to required one
def ori_in(org_img, scale):
    (h, w) = org_img.shape[:2]
    if h > w and h > scale:
        return image_resize(org_img, None, scale)
    elif w > h and w > scale:
        return image_resize(org_img, scale, None)
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
