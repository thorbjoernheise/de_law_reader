"""
PDF to TIFF Converter

This script converts each page of a PDF to a TIFF file.

Requirements:
- PyMuPDF (fitz)
- Pillow (PIL)

Usage:

"""

import fitz
from PIL import Image

def process_page(page, output_filename):
    """
    Process a single page and save it as a TIFF file.

    :param page: Page object from the PDF document.
    :param output_filename: Output filename for the TIFF file.
    """
    # Convert the page to an image (scaled to 300dpi)
    image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
    pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

    # Convert to grayscale
    pil_image = pil_image.convert("L")

    # Binarization (thresholding)
    threshold = 127
    pil_image = pil_image.point(lambda p: p > threshold and 255)

    # Save the processed page as a TIFF file
    pil_image.save(output_filename, "TIFF", dpi=(300, 300), compression="tiff_deflate")

def process_pdf(input_pdf, output_folder):
    """
    Process the PDF and save each page as a TIFF file.

    :param input_pdf: Input PDF file path.
    :param output_folder: Output folder path.
    """
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    for page_number, page in enumerate(pdf_document.pages(), start=1):
        # Save the processed page as a TIFF file
        output_filename = f"{output_folder}/page_{page_number}.tif"
        process_page(page, output_filename)

    # Close the PDF document
    pdf_document.close()

if __name__ == "__main__":
    # Configuration
    INPUT_PDF_FILE = "input/bgbl1_1949_5.pdf"
    OUTPUT_FOLDER_PATH = "output"

    # Process the PDF and save each page as a TIFF file
    process_pdf(INPUT_PDF_FILE, OUTPUT_FOLDER_PATH)
