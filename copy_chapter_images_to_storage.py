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
        continue

    topics = list(chapter.to_dict().get("topics"))

    newTopics = list(topics)

    for j, item in enumerate(newTopics):
        id = item['id']
        name = item['title']
        print('id: ', id)
        images = item['images']
        for i, img in enumerate(images):
            if 'firebasestorage' not in img and 'googleapis' not in img:
                print(img)
                # timeStamp = int(time.time()*1000)
                filePath = f'{topic}/{id}/{id} solution_{i}.jpeg'
                if not os.path.exists(f'{topic}/{id}'):
                    os.makedirs(f'{topic}/{id}')
                if not os.path.exists(filePath):
                    time.sleep(1)
                    urlretrieve(img, f"{filePath}")
                else:
                    print('image already exist')
                newBlob = bucket.blob(f'Physics/{filePath}')
                # if not newBlob.exists():
                newBlob.upload_from_filename(
                    filePath, content_type='image/jpeg')
                newBlob.make_public()
                # else:
                #     print('blob already exists!')
                # newBlob.make_public()
                url = newBlob.public_url
                print(url)
                images[i] = url

        # print(solns)
        item.update({'images': images})
        newTopics[j] = item

    print(newTopics)
    if len(newTopics) != 0:
        chapter_ref = db.collection(u'courses').document(chapter.id)
        chapter_ref.update({'topics': newTopics})
        print(f'chapter: {topic} updated!')
    else:
        print('list cannot empty')
        print(f'chapter {topic} not updated!')
