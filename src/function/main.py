from google.cloud import storage
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
    client = storage.Client()
    print('Reading from Bucket: {}'.format(event['bucket']))
    bucket = client.get_bucket(event['bucket'])
    print('Reading the file to watermark: {}'.format(event['name']))
   
    if(not uploaded_file.endswith('.pdf')):
        print('Invalid file format uploaded..Function will not watermark')
        return

    blob = bucket.blob(event['name'])
    
    print_function_meta_data(context, event)
    
def print_function_meta_data(context, event):
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

def watermark_pdf():
    print('About to watermark pdf...')