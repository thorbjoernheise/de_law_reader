from PIL import Image
import pytesseract

# PATH
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Configuration
image_path = 'BGBL_Test.png'
output_filename = "output.txt"
custom_config = '--oem 3 --psm 6 -l deu -c tessedit_write_images=true'

# IMG
img = Image.open(image_path)

# OCR
text = pytesseract.image_to_string(img, config=custom_config)

# Save as text
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(text)

print(f'Ergebnisse in {output_filename}')
