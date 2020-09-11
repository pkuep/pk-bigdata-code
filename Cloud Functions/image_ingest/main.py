from google.cloud import storage
import requests
from datetime import datetime

def ingest_image(request):
    """Pull an image from the webcam and store it in GCS """

    # pull the image
    url = 'https://qt.exploratorium.edu/roofcam/Observatory/image.jpg'
    filename = f"webcam_fromfunction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"  # add a timestamp
    response = requests.get(url)

    # store it in GCS
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("pk-gcs")  # replace the bucket name with yours
    blob = bucket.blob(filename)
    blob.upload_from_string(response.content, content_type='image/png')