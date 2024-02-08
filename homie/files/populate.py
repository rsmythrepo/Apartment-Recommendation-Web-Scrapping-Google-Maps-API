import os

from .csv import CSVUploader


def run(file_path: str):
    csv_uploader = CSVUploader()
    csv_uploader.populate(file_path)


if __name__ == "__main__":
    file_path = os.argv[1]
    run(file_path)
