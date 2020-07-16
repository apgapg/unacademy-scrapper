import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
from firebase_admin import storage
import os
from urllib.request import urlretrieve

# Use a service account
cred = credentials.Certificate('./service.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'teaching-6b309.appspot.com'
})
db = firestore.client()

bucket = storage.bucket()


topic = input("Enter Course Name: ")
if not topic:
    exit('topic can\'t be empty of null')

docs = db.collection('courses').where(u'topic', u'==', topic).stream()

chapters = list(docs)

for chapter in chapters:
    #chapter = list(docs)[0]
    print('Chapter: ', chapter.to_dict().get('name'))
    topic = chapter.to_dict().get('name')
    if chapter.to_dict().get("topics") is None:
        exit('Topics is null!')

    topics = list(chapter.to_dict().get("topics"))

    for subTopic in topics:
        numerical_ref = db.collection(u'numericals').document(subTopic['id'])
        doc=numerical_ref.get()
        if doc.exists:
            new_soln={'images':subTopic['images'],'video':subTopic['video']}
            numerical_ref.update({'solutions':[new_soln]})
