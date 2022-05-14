#!/usr/bin/env python3

from PyPDF2 import PdfFileWriter, PdfFileReader

import os
import sys
import errno
import os

def generate_watermark(input_pdf_path, watermark_pdf_path):
    # validate if both files exist otherwise throw error
      
    with open(input_pdf_path, "rb") as input_pdf_stream:
        input_pdf = PdfFileReader(input_pdf_stream)

        with open(watermark_pdf_path, "rb") as watermark_pdf_stream:
            watermark_pdf = PdfFileReader(watermark_pdf_stream)
            
            watermark_page = watermark_pdf.getPage(0)
            merged_pdf = os.path.abspath(input_pdf_path)[:-4] +"_watermark.pdf"
            #using python library watermark file and write to output stream and close
    
            create_watermarked_file(input_pdf, watermark_page, merged_pdf)
            return merged_pdf

def create_watermarked_file(input_pdf, watermark_page, merged):
    print(f'Generating watermark file" {merged}')
    output = PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        pdf_page = input_pdf.getPage(i)
        pdf_page.mergePage(watermark_page)
        output.addPage(pdf_page)

    with open(merged, "wb") as merged_file:
        output.write(merged_file)

#Append the suffix watermark to input file name
    
if __name__ == "__main__":
    print("Enter pdf to watermark:")
    inputpdf = input()

    if not inputpdf.endswith(".pdf"):
        print("Please supply a valid pdf file with correct extension!!")
        sys.exit(-1)

    print("Enter watermark pdf:")
    watermark_pdf = input()
    
    if not os.path.exists(os.path.abspath(inputpdf)):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), inputpdf)
    
    if not os.path.exists(os.path.abspath(watermark_pdf)):
         raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), watermark_pdf)
    try:
        generate_watermark(os.path.abspath(inputpdf), os.path.abspath(watermark_pdf))
    except:
        print("Oops something went wrong")
        sys.exit(-1)
else:
    inputpdf = "input.pdf"
    watermark_pdf = "watermark.pdf"
    generate_watermark(os.path.abspath(inputpdf), os.path.abspath(watermark_pdf))

