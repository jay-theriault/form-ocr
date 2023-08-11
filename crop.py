def crop_text_region(img, details, start_words, end_words):
    '''
    Function to crop a region of text from an image based on given start and end words
    Inputs: 
        img (array) - image to be cropped
        details (dict) - dictionary containing the OCR output details ('text', 'left', 'top', 'height')
        start_words (list of str) - list of starting words to find the region to be cropped
        end_words (list of str) - list of ending words to find the region to be cropped
    Outputs: 
        cropped_img (array) - cropped image containing the region between start_words and end_words
    '''

    cropped_images = []

    # Function to find the index of a sublist within a larger list
    def find_sublist(sl, l):
        results = []
        for ind in (i for i, text in enumerate(l) if sl[0].lower() in text.lower()):
            for j, word in enumerate(sl):
                if sl[j].lower() not in l[ind + j].lower():
                    break

                if j == len(sl) - 1:
                    return ind

        return None

    # Get the indices of the start and end words in the OCR details
    start_words_index = find_sublist(start_words, details['text'])
    end_words_index = find_sublist(end_words, details['text'])

    # get pixel locations for the cropped image
    # l: left, r: right, y: top of image h: height
    l = details['left'][start_words_index]
    y = details['top'][start_words_index]
    h = details['height'][start_words_index]
    
    # If end words not found or contains a newline, crop till the end of the image
    r = img.shape[1] if end_words_index is None or '\n' in end_words else details['left'][end_words_index]

    # add 5 pixels of padding to the front
    l = max(l - 5, 0)
    
    # add 15 pixels of padding to top and bottom
    y = y - 15
    h = h + 30

    # Crop the image according to the computed pixel locations and return
    cropped_img = img[y:y+h, l:r]

    return cropped_img