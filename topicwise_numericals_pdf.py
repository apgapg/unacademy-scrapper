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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

topic = input("Enter Course Name: ")
if not topic:
   exit('topic can\'t be empty of null')


defaultCover = 'https://firebasestorage.googleapis.com/v0/b/teaching-6b309.appspot.com/o/extras%2F6.jpeg?alt=media&token=65bd6852-43c4-4148-a421-4b6125fbae25'

# Use a service account
cred = credentials.Certificate('./service.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'teaching-6b309.appspot.com'
})
db = firestore.client()

bucket = storage.bucket()

docs = db.collection('numericals').where('topic', '==', f'{topic}').stream()

chapterList = list(docs)
print('Found', f'{len(chapterList)} numericals...')


def addWatermark(imagePath):
    photo = Image.open(imagePath)
    # get dim of image
    w, h = photo.size
    # draw image
    drawing = ImageDraw.Draw(photo)
    # define font
    font = ImageFont.truetype('fonts/Nunito-SemiBold.ttf', 14)
    # init text
    text = '© IIT-JEE by Ayush P Gupta'
    text_w, text_h = drawing.textsize(text, font)
    # draw text
    pos = (w - text_w)/2, (h - text_h) - 10
    drawing.text(pos, text, fill="#263238", font=font)
    # save
    photo.save(imagePath, quality=100)


for item in chapterList:
    imgUrls1 = item.to_dict().get("solutions")[0].get("images")
    imgUrls = list(item.to_dict().get('images'))
    imgUrls.extend(list(imgUrls1))
    imgUrls.insert(0, defaultCover)
    print(imgUrls)
    title = item.to_dict().get("title")

    imgs = []
    for i, j in enumerate(imgUrls):
        print("downloading %s" % (j))
        if not os.path.exists(topic+'/'+title):
            if not os.path.exists(topic):
                os.mkdir(topic)
            os.mkdir(topic+'/'+title)
            print("Directory ", topic+'/'+title,  " Created ")
        else:
            print("Directory ", topic+'/'+title,  " already exists")
        fullfilename = os.path.join(f'{topic}/{title}', f'{i}.jpeg')
        if not os.path.exists(fullfilename):
            urlretrieve(j, f"{fullfilename}")
            addWatermark(fullfilename)

        imgs.append(fullfilename)

        # if not os.path.exists(f"{topic}/{title} {item.id}.pdf"):
        if os.path.getsize(fullfilename) == 72032:
            imgs.remove(fullfilename)
            print('Ignored: ', fullfilename)

    with open(f"{topic}/{title} {item.id}.pdf", "wb") as f:
        f.write(img2pdf.convert(imgs))
    
    filePath=f"{topic}/{title} {item.id}.pdf"

    newBlob = bucket.blob(f'chapter-pdf/{filePath}')
    newBlob.upload_from_filename(filePath, content_type='application/pdf')
    newBlob.make_public()

