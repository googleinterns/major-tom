import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

default_app = firebase_admin.initialize_app()

# /home/jaimehisao2011/.config/gcloud/application_default_credentials.json

def get_regulation_documents():
    db = firestore.client()
    reg_ref = db.collection('regulation_documents')
    return reg_ref.stream()


def get_article(id):
    return db.collection(u'articles').document(u''.format(id))
