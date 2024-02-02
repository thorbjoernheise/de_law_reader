"""
OCR via Tesseract

This script performs OCR (Optical Character Recognition) on a given image using Tesseract
and saves the results to a text file.

Requirements:
- Tesseract OCR
- Pillow (PIL)

Usage:
python ocr_tesseract.py
"""

from PIL import Image
import pytesseract

def perform_ocr(image_path, output_filename, custom_config):
    """
    Perform OCR on the given image and save the results to a text file.

    :param image_path: Path to the input image.
    :param output_filename: Output filename for the text file.
    :param custom_config: Custom Tesseract configuration.
    """
    # Set Tesseract path
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    # Open the image
    img = Image.open(image_path)

    # Perform OCR
    text = pytesseract.image_to_string(img, config=custom_config)

    # Save the results as text
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f'Results saved to {output_filename}')

if __name__ == "__main__":
    # Configuration
    IMAGE_PATH = 'output/page_1.tif'
    OUTPUT_FILENAME = "output/output.txt"
    CUSTOM_CONFIG = '--oem 1 --psm 6 -l deu -c tessedit_write_images=false'

    # Perform OCR and save results
    perform_ocr(IMAGE_PATH, OUTPUT_FILENAME, CUSTOM_CONFIG)
