import os
import tempfile
from PyPDF2 import PdfFileReader, PdfFileWriter
from google.cloud import storage

storage_client = storage.Client()

watermark_file_name = 'watermark.pdf'
   
def watermark_file(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    output_bucket_name = os.environ.get('WATERMARK_OUTPUT_BUCKET_NAME')
    print(f'Output bucket: {output_bucket_name}')
    
    print_function_meta_data(context, event)

    uploaded_file = event['name']
    input_bucket_name = event["bucket"]
    
    if(not uploaded_file.endswith('.pdf')):
        print('Invalid file format uploaded..Function will not watermark')
        return
   
    print('Reading from Bucket: {}'.format(event['bucket']))
    print('Reading the file to watermark: {}'.format(event['name']))
   
    input_blob = storage_client.bucket(input_bucket_name).get_blob(uploaded_file)
    watermark_blob = storage_client.bucket(output_bucket_name).get_blob(watermark_file_name)

    if(watermark_blob == None):
        print('Failed to read: {} from cloud storage. Function cannot watermark!!'.format(watermark_file_name))
        return

    watermark_pdf(input_blob, watermark_blob)
    
def print_function_meta_data(context, event):
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

def watermark_pdf(blob_to_watermark, blob_to_merge):
    print('About to watermark pdf...')
    file_name = blob_to_watermark.name
    watermark_file_name = blob_to_merge.name

    inputblob_local_filename = tempfile.mktemp()
    watermarkblob_local_filename = tempfile.mktemp()

    # Download uploaded pdf from bucket.
    blob_to_watermark.download_to_filename(inputblob_local_filename)
    print(f"Pdf {file_name} was downloaded to {inputblob_local_filename}.")
    blob_to_merge.download_to_filename(watermarkblob_local_filename)
    print(f"Pdf {watermark_file_name} was downloaded to {watermarkblob_local_filename}.")
    
    input_pdf = PdfFileReader(inputblob_local_filename)
    watermark_pdf = PdfFileReader(watermarkblob_local_filename)
    watermark_page = watermark_pdf.getPage(0)
    waternarked_file_name = os.path.splitext(file_name)[0]+"_watermarked.pdf"
    mergedfile =  os.path.abspath(inputblob_local_filename).split('.')[0] + "_watermarked.pdf"
    #using python library watermark file and write to output stream and close
    print(f'Generating watermark file" {mergedfile}')
    
    output = PdfFileWriter()

    for page in range(input_pdf.getNumPages()):
        pdf_page = input_pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        output.addPage(pdf_page)

    with open(mergedfile, "wb") as merged_file:
        output.write(merged_file)

    output_bucket = storage_client.get_bucket('watermarkoutput')

    blob = output_bucket.blob(waternarked_file_name)
    blob.upload_from_filename(mergedfile)
