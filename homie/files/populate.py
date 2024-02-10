import os

from homie.files.csv import FlatCSVUploader


def run(file_path: str):
    csv_uploader = FlatCSVUploader()
    csv_uploader.populate(file_path)


if __name__ == "__main__":
    file_path = os.argv[1]
    run(file_path)
