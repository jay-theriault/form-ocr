# standard imports
import numpy as np 
import pandas as pd 
import numpy as np
import sys

# non-standard imports
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# import functions from my files
from image_preprocessing import load_image_and_preprocess, remove_horizontal_lines
from parse_ocr import get_most_common_option, parse_date, extract_materials
from crop import crop_text_region

if __name__ == '__main__':
    
    try:
        image_path = sys.argv[1]
    except IndexError as e:
        image_path = "Images/Image_1.jpg"
    
    # Load and preprocess image
    img = load_image_and_preprocess(image_path)
    height, width = img.shape

    # get image details
    details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Get cropped image for relevant region using pytessaract
    # This should mostly generalize since the printed characters should always be recognizable
    # but if I was designing this for long term use I would probably crop to an area of the paper
    # and not the words since the words may be written over. But that would require resizing the images
    # and more work than just looking for the sections in this one image
    start_words = ['Water', 'Conn', 'Size']
    end_words = ['Sanitary']
    water_conn_img = crop_text_region(img, details, start_words, end_words)

    start_words = ['Meter', 'Size', 'Installed']
    end_words = ['Meter', 'Install', 'Date']
    meter_size_img = crop_text_region(img, details, start_words, end_words)

    start_words = ['Meter', 'Install', 'Date']
    end_words = ['Meter', 'No']
    meter_date_img = crop_text_region(img, details, start_words, end_words)

    start_words = ['Materials', 'Used']
    end_words = ['\n']
    materials_img = crop_text_region(img, details, start_words, end_words)

    # Extract relevant information from each image
    results = {}

    # get text from both the image with line and line removed, to see if either gets a better read from OCR
    # for this example without lines performs better but that is not necessarily always the case
    # for water conn size and meter size installed we find what numbers are in the image and try to match them to known values
    # this is easy for this situation since the digits are unique across the different options but this would be more difficult 
    # if the options shared common digits
    water_conn_nums = pytesseract.image_to_string(water_conn_img, config='--psm 6 outputbase digits')
    water_conn_nums_noline = pytesseract.image_to_string(remove_horizontal_lines(water_conn_img), config='--psm 6 outputbase digits')
    results['Water Conn Size'] = get_most_common_option(water_conn_nums, water_conn_nums_noline, ['3/4"', '5/8"'])

    meter_size_nums = pytesseract.image_to_string(meter_size_img, config='--psm 6 outputbase digits')
    meter_size_nums_noline = pytesseract.image_to_string(remove_horizontal_lines(meter_size_img), config='--psm 6 outputbase digits')
    results['Meter Size Installed'] = get_most_common_option(meter_size_nums, meter_size_nums_noline, ['5/8 x 3/4', '2'])

    # for meter date we try and parse a date from each of the line and no line images
    # then we output the date with the highest precision
    # pytessaract can't seem to figure out that there is an 11 between the 8- and the -2020 even though its clear as day in
    # the cropped image but I'm sure paid OCR like Google Cloud Vision would be able to pick it up better 
    meter_date_nums = pytesseract.image_to_string(meter_date_img, config='--psm 6 outputbase digits')
    meter_date_nums_noline = pytesseract.image_to_string(remove_horizontal_lines(meter_date_img), config='--psm 6 outputbase digits')
    results['Meter Date'] = parse_date(meter_date_nums, meter_date_nums_noline)

    # For materials this is the one where pytessaract's handwriting struggles the most. Removing the line helps a lot but it's
    # still pretty bad, again with the paid versions it's probably better. We try and match as many words as we can to the known
    # words using fuzzywuzzy and we output it as a string with commas separating the different materials used. If I spent more time
    # I could maybe figure out how to get the amount of material used by each, and again better handwriting recognition would definately
    # help.
    materials_str = pytesseract.image_to_string(remove_horizontal_lines(materials_img))
    results['Materials'] = extract_materials(materials_str)

    # convert dictionary to pandas dataframe and then save to csv
    results_df = pd.DataFrame.from_dict({k: [v] for k, v in results.items()})
    results_df.to_csv('results.csv', index=False)



