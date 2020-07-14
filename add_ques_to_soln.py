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

docs = db.collection('numericals').order_by(
    'createdAt', direction=firestore.Query.DESCENDING).stream()

chapterList = list(docs)
newList = chapterList[25:len(chapterList)]

for item in newList:
    quesImg = item.to_dict().get("images")[0]
    solnImgs = item.to_dict().get("solutions")[0].get("images")
    print(quesImg)
    if quesImg in solnImgs:
        print('Question image already in soln')
        continue
    else:
        print('Question not present')
    solnImgs.insert(0, quesImg)

    
    
    # newSoln = item.to_dict().get("solutions")[0]
    # newSoln.update({'images': solnImgs})
    # db.collection('numericals').document(f'{item.id}').set({
    #         'solutions': [
    #             newSoln
    #         ],
    #     }, merge=True)
