import cv2
import numpy as np

ref_point = []

def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point.append((x, y))

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))


def mark_image(uploaded_file):
    # load the image, clone it, and set up the mouse callback function
    img = cv2.imread(uploaded_file, cv2.IMREAD_COLOR)
    copy = img.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        # cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or len(ref_point) == 5:
            break

        # draw a rectangle around the region of interest
        if len(ref_point) == 2:
            cv2.rectangle(img, ref_point[0], ref_point[1], (0, 255, 0), 2)
        if len(ref_point) == 4:
            cv2.rectangle(img, ref_point[2], ref_point[3], (255, 0, 0), 2)
        cv2.imshow("image", img)

    cv2.destroyAllWindows()
    if len(ref_point) != 0:
        create_new_image(ref_point[0], ref_point[1], src=copy, character="A")
    if len(ref_point) >= 4:
        create_new_image(ref_point[2], ref_point[3], src=copy, character="B")
    return copy


def create_new_image(top_left, bottom_right, src, character):
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]

    image = np.zeros((height, width, 3), np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x] = src[y + top_left[1], x + top_left[0]]

    filepath = ("./static/classified_images/yoshi" + character + ".png")
    cv2.imwrite(filename=filepath, img=image, params=(cv2.IMWRITE_PNG_COMPRESSION, 1))  # 1 - compression, 0 - no compression
