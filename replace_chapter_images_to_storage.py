import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time

# Use a service account
cred = credentials.Certificate('./service.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# topic = input("Enter Course Name: ")
# if not topic:
#     exit('topic can\'t be empty of null')

docs = db.collection('courses').stream()

chapters = list(docs)

for chapter in chapters:
    #chapter = list(docs)[0]
    print('Chapter: ', chapter.to_dict().get('name'))
    if chapter.to_dict().get("topics") is None:
        continue

    topics = list(chapter.to_dict().get("topics"))

    newTopics = list(topics)

    for i, item in enumerate(topics):
        id = item['id']
        print('id: ', id)
        doc_ref = db.collection(u'numericals').document(f'{id}')
        doc = doc_ref.get()
        if doc.exists:
            print(doc.to_dict()['title'])
            solns = doc.to_dict()['solutions'][0]['images']
            # print(solns)
            item.update({'images': solns})
            newTopics.pop(i)
            newTopics.insert(i, item)
        else:
            print(id, ' doesnt exist!')

    print(newTopics)
    if len(newTopics) != 0:
        chapter_ref = db.collection(u'courses').document(chapter.id)
        chapter_ref.update({'topics': newTopics})
    else:
        print('list cannot empty')
