import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, firestore
from firebase_admin.storage import bucket

from src.firebase.storage.bucket import Bucket
from src.firebase.storage.image_object import ImageObjectOnBucket
from src.utils.logger import logger

load_dotenv()


class Firebase:
    CREDENTIALS = {"type": "service_account",
                   "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET'],
                   "project_id": os.environ["FIREBASE_PROJECT_ID"],
                   "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
                   "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
                   "client_email": os.environ["FIREBASE_CLIENT_EMAIL"], "client_id": os.environ["FIREBASE_CLIENT_ID"],
                   "auth_uri": os.environ["FIREBASE_AUTH_URI"], "token_uri": os.environ["FIREBASE_TOKEN_URI"],
                   "auth_provider_x509_cert_url": os.environ["FIREBASE_CERT_URL"],
                   "client_x509_cert_url": os.environ["FIREBASE_CERT_CLIENT_URL"],
                   "universe_domain": os.environ["FIREBASE_UNIVERSE_DOMAIN"], }

    def __init__(self):
        logger.info("reading certificates of firebase")
        self._certificate = firebase_admin.credentials.Certificate(Firebase.CREDENTIALS)

        logger.info("checking if has an firebase app to load!")
        if len(firebase_admin._apps.keys()) == 0:
            logger.info("initializing firebase app")
            self._application: firebase_admin.App = firebase_admin.initialize_app(credential=self._certificate,
                                                                                  options=Firebase.CREDENTIALS)
        else:
            logger.info("using existing firebase app")
            self._application = firebase_admin._apps[list(firebase_admin._apps.keys())[0]]

        logger.info("initializing bucket")
        self.storage = bucket(app=self._application)
        self.auth = auth
        self.firestore = firestore.client(app=self._application)

        logger.success("firebase is up!!")

    @property
    def application(self):
        return self._application


firebase = Firebase()
