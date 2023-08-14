# form-ocr
## Description
form-ocr is a Python project designed to extract information from scanned utility forms using the open-source OCR library pytesseract. It leverages the capabilities of Tesseract OCR to analyze images of forms and retrieve key details, thus automating the manual process of data extraction from paper documents.

## Requirements
- Python 3.x
- Tesseract OCR
- pytesseract

## Installation
**Install Python:** Ensure that Python 3.x is installed on your system. If not, you can download it from [here](https://www.python.org/downloads/).

**Install Tesseract OCR:** form-ocr relies on Tesseract OCR, which must be installed on your system. Follow the instructions provided on the [official website](https://github.com/tesseract-ocr/tesseract) to install Tesseract OCR for your operating system.

**Install pytesseract:** You can install the pytesseract library using pip:

``` python
pip install pytesseract
```

## Usage
You can use form-ocr to process a scanned utility form by executing the main script, providing the path to the image as an argument.

Example:

``` python
python main.py path/to/your/image.png
```

## Contributions
Feel free to fork the repository, make some improvements, and create pull requests. All contributions are welcome!

## License
[MIT License](url)
