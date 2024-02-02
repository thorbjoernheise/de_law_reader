import fitz
from PIL import Image

def process_page(page, output_filename):

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
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    for page_number, page in enumerate(pdf_document.pages(), start=1):
        # Save the processed page as a TIFF file
        name = input_pdf.split('.')[0]
        if "/" in name:
            name = name.split('/')[1]
        output_filename = f"{output_folder}/{name}_{page_number}.tif"
        print(f"Saved page {page_number} to {output_filename}")
        process_page(page, output_filename)

    # Close the PDF document
    pdf_document.close()

