from abc import ABC, abstractmethod

from src.firebase.storage.image_object import ImageObjectOnBucket


class Bucket(ABC):
    def __init__(self, name: str, docs_link: str):
        self._name = name
        self._docs_link = docs_link

        self._application = None

    @abstractmethod
    def upload_image(self, image_path: str) -> ImageObjectOnBucket:
        """Upload image to a bucket
        :param image_path:
        :return: image path on bucket
        :rtype: str
        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def docs(self):
        return self._docs_link

    @property
    @abstractmethod
    def application(self):
        ...

    def __repr__(self):
        return f"<Bucket name='{self._name}' docs='{self._docs_link}'>"

    def __str__(self):
        return f"<Bucket name='{self._name}' docs='{self._docs_link}'>"
