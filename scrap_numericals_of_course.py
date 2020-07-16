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

subject='Physics'
topic='Motion in One Dimension'
courseUrl='https://unacademy.com/course/motion-in-one-dimension-for-iit-jee/2XZN4YY4'

html = urlopen(courseUrl)
bs = BeautifulSoup(html.read(), 'html.parser')

nameList = bs.find('div', {'class': 'Week__Wrapper-sc-1qeje5a-2 hLDUrW'}
                   ).findAll('a', {'class': 'Link__StyledAnchor-sc-1n9f3wx-0 kOEPuX'})
for name in nameList:
    url = 'https://unacademy.com'+name.attrs['href']
    title = name.find('h6', {'class': 'H6-sc-1gn2suh-0 jMZxgl'}).get_text()
    print(title)
    if 'Quality Numerical' not in title:
        continue
    childBs = BeautifulSoup(urlopen(url).read(), 'html.parser')
    uid = childBs.find(
        'meta', {'property': 'twitter:image'}).attrs['content'].split('/')[3]
    print(uid)

    doc_ref = db.collection(u'numericals').document(f'{uid}')
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document exists: {uid}')
        continue

    response = urlopen(
        'https://player.uacdn.net/lesson-raw/%s/events-data.json' % (uid))
    data = json.load(response)
    rawImgSeq = list(map(lambda y: y.get('i'), list(
        filter(lambda x: 'i' in x, data))))
    rawImgSeq2 = list(dict.fromkeys(rawImgSeq))
    imgSeq = list(
        map(lambda x: 'https://edge.uacdn.net/%s/images/%s.jpeg' % (uid, x), rawImgSeq2))
    print(imgSeq)

    if len(imgSeq) > 0:
        db.collection('numericals').document(f'{uid}').set({
            'title': title.replace('Quality Numerical ',''),
            'level': 1,
            'subject': subject,
            'topic': topic,
            'images': [imgSeq[2]],
            'solutions': [
                {
                    'images': imgSeq,
                    'video': url,
                }
            ],
            'createdAt': int(time.time()*1000),
        }, merge=True)

print(len(nameList))
