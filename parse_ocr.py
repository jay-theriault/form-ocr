from fuzzywuzzy import fuzz
import numpy as np
from collections import Counter
from datetime import datetime

def get_most_common_option(scraped_str1, scraped_str2, option_strs):
    '''
    Function to return the most common option string in two given strings. In case of a tie, return None.
    Inputs: 
        scraped_str1, scraped_str2 (str) - Strings to search in.
        option_strs (list of str) - List of option strings to count.
    Outputs: 
        most_common_option (str) - Most common option string or None if there is a tie or no matches.
    '''

    counter = Counter()
    for scraped_str in [scraped_str1, scraped_str2]:
        for digit in scraped_str:
            for option_str in option_strs:
                if digit in option_str:
                    counter[option_str] += 1
    
    most_common = counter.most_common(2)  # get two most common option strings
    
    # if there are multiple option strings with the same highest count, return NaN
    if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
        return None
    
    if most_common:
        return most_common[0][0]  # return the option string with the most occurrences
    
    return None  # return None if no option string matches

def parse_date(str1, str2):
    '''
    Function to parse two date strings and return the most precise one.
    Inputs: 
        str1, str2 (str) - Date strings.
    Outputs: 
        date (datetime) - Most precise date or None if both inputs are not valid dates.
    '''

    date1 = parse_date_str(str1)
    date2 = parse_date_str(str2)
    return get_most_precise_date(date1, date2)

def parse_date_str(input_str):
    '''
    Function to parse a date string and return it as a datetime object. Incomplete dates are filled with default values.
    Inputs: 
        input_str (str) - Date string.
    Outputs: 
        date (datetime) - Parsed date or None if input_str is not a valid date.
    '''

    # Strip leading/trailing whitespaces and control characters
    input_str = input_str.strip()

    # Determine the separator based on the input string
    split_char = '-' if '-' in input_str else '/'

    # Split the string into components
    parts = [int(part) if part.isdigit() else None for part in input_str.split(split_char)]

    # Extend the parts list to 3 elements (for month, day, year) if it's not already
    parts.extend([None] * (3 - len(parts)))

    month, day, year = parts

    # Handle two-digit years
    if year is not None and year < 100:
        if year < 50:  # Handle the 2000s
            year += 2000
        else:  # Handle the 1900s
            year += 1900
    
    # Construct date string
    date_str = f"{year or ''}-{month or '01'}-{day or '01'}"
    
    # Parse date string into a datetime object
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:  # Handle incomplete dates
        date = None

    return date

def get_most_precise_date(date1, date2):
    '''
    Function to return the most precise date of two given dates. If one date is None, the other is returned.
    Inputs: 
        date1, date2 (datetime) - Dates.
    Outputs: 
        date (datetime) - Most precise date or None if both inputs are None.
    '''

    # Handle cases where one or both dates are None
    if date1 is None and date2 is None:
        return None
    elif date1 is None:
        return date2
    elif date2 is None:
        return date1

    # If both dates exist, determine which is more precise
    precision1 = (date1.year is not None, date1.month is not None, date1.day is not None)
    precision2 = (date2.year is not None, date2.month is not None, date2.day is not None)

    if precision1 > precision2:
        return date1
    else:
        return date2

def extract_materials(input_str, fuzzy_thresh=75):
    '''
    Function to extract materials from an input string based on fuzzy string matching with a list of common materials.
    Inputs: 
        input_str (str) - String to extract materials from.
        fuzzy_thresh (int) - Threshold for fuzzy string matching. Default is 75.
    Outputs: 
        materials (str) - Comma-separated string of found materials or empty string if none found.
    '''
    
    # Define a list of common words/materials
    common_words = ["Copper", "Corp. Stop", "Angle", "Meter", "Brackets"]

    # Initialize an empty list to store the materials found
    found_materials = []

    # Clean the input string
    input_str = input_str.lower().replace("materials used:", "").strip()

    # Loop over the common words/materials
    for word in common_words:
        # Loop over the words in the input string
        for input_word in input_str.split():
            # If a common word is similar enough to an input word, add it to the found_materials list
            if fuzz.ratio(word.lower(), input_word) > fuzzy_thresh:  # You may adjust this threshold based on your needs
                found_materials.append(word)
                break

    return ', '.join(found_materials)