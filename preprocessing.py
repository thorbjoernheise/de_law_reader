import fitz
from PIL import Image

def process_pdf(input_pdf, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    for page_number in range(pdf_document.page_count):
        # Extract each page from the PDF
        page = pdf_document.load_page(page_number)

        # Convert the page to an image (scaled to 300dpi)
        image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Convert to grayscale
        pil_image = pil_image.convert("L")

        # Binarization (thresholding)
        threshold = 127
        pil_image = pil_image.point(lambda p: p > threshold and 255)

        # Save the processed page as a TIFF file
        output_filename = f"{output_folder}/page_{page_number + 1}.tif"
        pil_image.save(output_filename, "TIFF", dpi=(300, 300), compression="tiff_deflate")

    # Close the PDF document
    pdf_document.close()

if __name__ == "__main__":
    # Specify the input PDF file and output folder
    input_pdf_file = "input.pdf"
    output_folder_path = "output_folder"

    # Process the PDF and save each page as a TIFF file
    process_pdf(input_pdf_file, output_folder_path)
