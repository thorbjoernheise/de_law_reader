from PIL import Image
import pytesseract

def perform_ocr(image_path, output_filename, custom_config):
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

