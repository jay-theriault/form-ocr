import cv2

def fix_skew(img):
    '''
    Function to straighten a rotated image so that OCR works better
    Inputs: img (array) - image to be straightened
    Outputs: img (array) - straightened image
    '''

    # Get the skew angle of the image
    angle = get_skew_angle(img)
    
    # Return the rotated image to fix the skew
    return rotate_img(img, angle)


def get_skew_angle(img):
    '''
    Function to compute the skew angle of an image
    Inputs: img (array) - image to be analysed
    Outputs: angle (float) - skew angle of the image
    '''

    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = img.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle

    return angle

def rotate_img(img, angle: float):
    '''
    Function to rotate an image by a specific angle
    Inputs: img (array) - image to be rotated
            angle (float) - angle by which image is to be rotated
    Outputs: newImage (array) - rotated image
    '''

    newImage = img.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def load_image_and_preprocess(image_path):
    '''
    Function to load an image and preprocess it by fixing skew and converting to grayscale
    Inputs: image_path (str) - path to the image to be loaded
    Outputs: img (array) - preprocessed image
    '''

    # Load the image
    img = cv2.imread(image_path)

    # rotate the image to fix any skew
    img = fix_skew(img)

    # Convert the image to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img

def remove_horizontal_lines(img):
    # Use Otsu's threshold to obtain a binary image
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal lines
    img = remove_horizontal_lines_kernel(img, img, dark=True, l=50)

    # revert back to white and black
    img = cv2.bitwise_not(img)

    return img

def remove_horizontal_lines_kernel(img, thresh, dark=False, l=25):
    '''
    Function to remove horizontal lines from an image using a kernel
    Inputs: img (array) - image from which lines are to be removed
            thresh (array) - thresholded image for line detection
            dark (bool) - if True, uses a black pen to draw contours; if False, uses a white pen
            l (int) - length of the horizontal kernel
    Outputs: result (array) - image with lines removed
    '''

    # Define horizontal kernel and use morphology operations to detect lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (l,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    # Draw over the detected lines with black or white color
    for c in cnts:
        cv2.drawContours(img, [c], -1, (0,0,0), 2) if dark else cv2.drawContours(img, [c], -1, (255, 255, 255), 2)

    # # Repair image
    # repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,6))
    # result = 255 - cv2.morphologyEx(255 - img, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
    
    # Copy image into result
    result = img.copy()

    return result