import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
import time
import os
import img2pdf
from firebase_admin import storage

# Use a service account
cred = credentials.Certificate('./service.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'teaching-6b309.appspot.com'
})
db = firestore.client()

bucket = storage.bucket()

all_blobs = list(bucket.list_blobs(
    prefix='chapter-pdf/Rotational Mechanics/'))
blob_names = list(map(lambda x: x.name, all_blobs))

pdfBlobs = list(filter(lambda x: '.pdf' in x, blob_names))

dBlob = bucket.get_blob(pdfBlobs[0])
print(dBlob.name)

filePath = 'Rotational Mechanics/001 : Angular Acceleration of Pulley PC6D9IRCBEELYCRH0L9A.pdf'

newBlob = bucket.blob(f'chapter-pdf/{filePath}')
newBlob.upload_from_filename(filePath, content_type='application/pdf')
newBlob.make_public()
