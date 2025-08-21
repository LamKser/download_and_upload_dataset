import json
import string
import re

import gdown
from kaggle.api.kaggle_api_extended import KaggleApi

FOLDER_URL = "https://drive.google.com/drive/folders"
FILE_URL = "https://drive.google.com/uc?id="

api = KaggleApi()
api.authenticate()

def correct_slug_name(slug: str):
    slug = slug.lower()
    special_character = string.punctuation.replace('-', '') + ' '
    special_character = f"[{re.escape(special_character)}]"
    # Get index of special characters
    indices = [match.start() for match in re.finditer(special_character, slug)]
    list_slug = list(slug)
    for idx in indices:
        list_slug[idx] = '-'
    slug = ''.join(list_slug)
    return slug

def download_gg_drive(id_: str, output: str = "output"):
    download_url = FOLDER_URL + '/' + id_
    gdown.download_folder(download_url, output=output)


def upload_kaggle(folder: str, title: str, public_data: bool = True):
    # Check title
    if ' ' in title:
        raise ValueError(
            "Title should contain alphanumeric or "-" characters"
        )
    api.dataset_initialize(folder=folder)
    with open(f"{folder}/dataset-metadata.json", 'r') as f:
        data = json.load(f)
        data["title"] = title
        data["id"] = data["id"].split('/')[0] + '/' + correct_slug_name(title)

    with open(f"{folder}/dataset-metadata.json", 'w') as f:
        json.dump(data, f, indent=4)

    api.dataset_create_new_cli(
        folder=folder,
        public=public_data
    )
    
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Download data from Google Drive and Upload to Kaggle")
    parser.add_argument("--folder", action="store_true", help="Download mode (Default: file)")
    parser.add_argument("--id", type=str, required=True, help="ID of google url")
    parser.add_argument("--save", type=str, default="output", help="Save download directory (Default: \"output\")")
    parser.add_argument("--title", type=str, default="data", help="Title of dataset (Default: \"data\")")
    parser.add_argument("--public", action="store_true", help="Public dataset")
    args = parser.parse_args()
    
    if args.folder:
        print(" Downloading \"FOLDER\" from Google Drive ".center(50, '='))
        download_gg_drive(args.id, args.save)
    print(" Uploading to Kaggle ".center(50, '='))
    upload_kaggle(args.save, args.title, args.public)

