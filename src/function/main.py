import os
import tempfile
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from google.cloud import storage

storage_client = storage.Client()
output_bucket_name = os.getenv("WATERMARK_OUTPUT_BUCKET_NAME")
   
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
    print('instantiating storage client')
    uploaded_file = format(event['name'])
    input_bucket_name = event["bucket"]
    
    if(not uploaded_file.endswith('.pdf')):
        print('Invalid file format uploaded..Function will not watermark')
        return
   
    storage_client = storage.Client()
    print('Reading from Bucket: {}'.format(event['bucket']))
    print('Reading the file to watermark: {}'.format(event['name']))
   
    input_blob = storage_client.bucket(input_bucket_name).get_blob(uploaded_file)
    watermark_blob = storage_client.bucket(output_bucket_name).get_blob('watermark.pdf')
   
    print_function_meta_data(context, event)
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
    waternarked_file_name = file_name+"watermark.odf"
    mergedfile = os.path.abspath(inputblob_local_filename).split('.')[0] +"watermark.pdf"
    #using python library watermark file and write to output stream and close
    print(f'Generating watermark file" {mergedfile}')
    
    output = PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        pdf_page = input_pdf.getPage(i)
        pdf_page.mergePage(watermark_page)
        output.addPage(pdf_page)

    with open(mergedfile, "wb") as merged_file:
        output.write(merged_file)

    output_bucket = storage_client.get_bucket('watermarkoutput')

    blob = output_bucket.blob(waternarked_file_name)
    blob.upload_from_filename(mergedfile)

    