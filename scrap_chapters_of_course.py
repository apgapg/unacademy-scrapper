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

subject = 'Physics'
topic = 'Simple Harmonic Motion'
courseUrl = 'https://unacademy.com/course/simple-harmonic-motion-for-iit-jee/8U80RYEN'

courseUid = courseUrl.split('/')[5]
print('course UID: ', courseUid)

html = urlopen(courseUrl)
bs = BeautifulSoup(html.read(), 'html.parser')

nameList = bs.find('div', {'class': 'Week__Wrapper-sc-1qeje5a-2 hLDUrW'}
                   ).findAll('a', {'class': 'Link__StyledAnchor-sc-1n9f3wx-0 kOEPuX'})
topics = []
for name in nameList:
    url = 'https://unacademy.com'+name.attrs['href']
    title = name.find('h6', {'class': 'H6-sc-1gn2suh-0 jMZxgl'}).get_text()
    print(title)
    # if 'Quality Numerical' not in title:
    #     continue
    time.sleep(4)

    childBs = BeautifulSoup(urlopen(url).read(), 'html.parser')
    uid = childBs.find(
        'meta', {'property': 'twitter:image'}).attrs['content'].split('/')[3]
    print(uid)
    time.sleep(4)
    response = urlopen(
        'https://player.uacdn.net/lesson-raw/%s/events-data.json' % (uid))
    data = json.load(response)
    rawImgSeq = list(map(lambda y: y.get('i'), list(
        filter(lambda x: 'i' in x, data))))
    rawImgSeq2 = list(dict.fromkeys(rawImgSeq))
    imgSeq = list(
        map(lambda x: 'https://edge.uacdn.net/%s/images/%s.jpeg' % (uid, x), rawImgSeq2))
    print(imgSeq)
    print('Found images: ',len(imgSeq))
    myTopic = {
        'id':uid,
        'title': title,
        'video': url,
        'images': imgSeq,
        'createdAt': int(time.time()*1000),
    }
    topics.append(myTopic)

db.collection('courses').document(f'{courseUid}').set({
    'title': topic,
    'name': topic,
    'subject': subject,
    'topic': topic,
    'videoLink': courseUrl,
    'createdAt': int(time.time()*1000),
    'topics': topics,
}, merge=True)

print(len(nameList))
