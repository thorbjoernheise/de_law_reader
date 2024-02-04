import sys
from preprocessing import process_pdf
import os
from ocr import perform_ocr

def main():
    try:
        # Check if the correct number of command-line arguments is provided
        if len(sys.argv) != 2 or sys.argv[1] == "-h":
            raise ValueError("Please enter the path to your .pdf file. Use -h or -help for help.")

        # Input PDF file path from command-line argument
        input_pdf = sys.argv[1]
        output_folder = "output"

        """
        Preprocessing
        """
        process_pdf(input_pdf, output_folder)

        """
        OCR
        """
        
        for tiff_file in os.listdir(output_folder):
            if tiff_file.endswith(".tif"):
                tiff_path = os.path.join(output_folder, tiff_file)
                page_number = tiff_file.split("_")[1].split(".")[0]  # Extract page number from the filename

                # Output text file path
                output_text_file = os.path.join(output_folder, f"page_{page_number}.txt")

                print(f"Performing OCR on {tiff_file}...")
                custom_config = '--oem 1 --psm 6 -l deu -c tessedit_write_images=false'
                perform_ocr(tiff_path, output_text_file, custom_config)
                #subprocess.run(["python", "ocr.py", tiff_path, output_text_file])

        print("Process completed successfully.")



    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main()
