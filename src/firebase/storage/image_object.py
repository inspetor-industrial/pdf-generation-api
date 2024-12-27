from typing import Any


class ImageObjectOnBucket:
    def __init__(self, name: str, size: int, download_url: str, fileid_on_drive: str):
        self._name = name
        self._size = size
        self._download_url = download_url
        self._fileid_on_drive = fileid_on_drive

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "size": self._size,
            "downloadUrl": self._download_url,
            "rawFile": "",
            "fileIdOnDrive": self._fileid_on_drive
        }