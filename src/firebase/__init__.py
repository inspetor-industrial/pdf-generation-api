import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin.storage import bucket

from src.firebase.storage.bucket import Bucket
from src.firebase.storage.image_object import ImageObjectOnBucket
from src.utils.logger import logger

load_dotenv()


class FirebaseStorage:
    CREDENTIALS = {"apiKey": os.environ["FIREBASE_API_KEY"], "authDomain": os.environ["FIREBASE_AUTH_DOMAIN"],
                   "projectId": os.environ["FIREBASE_PROJECT_ID"],
                   "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
                   "messagingSenderId": os.environ["FIREBASE_MESSAGING_SENDER_ID"],
                   "appId": os.environ["FIREBASE_APP_ID"], "measurementId": os.environ["FIREBASE_MEASUREMENT_ID"], }

    def __init__(self):
        logger.info("reading certificates of firebase")
        self._certificate = firebase_admin.credentials.Certificate(FirebaseStorage.CREDENTIALS)

        logger.info("checking if has an firebase app to load!")
        if len(firebase_admin._apps.keys()) == 0:
            logger.info("initializing firebase app")
            self._application: firebase_admin.App = firebase_admin.initialize_app(credential=self._certificate,
                                                                                  options=FirebaseStorage.CREDENTIALS)
        else:
            logger.info("using existing firebase app")
            self._application = firebase_admin._apps[list(firebase_admin._apps.keys())[0]]

        logger.info("initializing bucket")
        self._storage = bucket(app=self._application)

        logger.success("firebase is up!!")

    @property
    def application(self):
        return self._application
