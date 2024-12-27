from abc import ABC, abstractmethod
from pathlib import Path


class FileUtils(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def check_if_page_exists(filepath: Path) -> bool:
        does_exists_report_filepath = filepath.exists()
        if does_exists_report_filepath:
            return True

        raise FileExistsError("Report file does not exists!")
