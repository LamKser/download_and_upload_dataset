import gdown
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import json

api = KaggleApi()
api.authenticate()

def download_gg_drive(id_: str, url: str = "https://drive.google.com/drive/folders/", output: str = "output"):
    download_url = url + id_
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
        data["id"] = data["id"].split('/')[0] + '/' + title

    with open(f"{folder}/dataset-metadata.json", 'w') as f:
        json.dump(data, f, indent=4)

    api.dataset_create_new_cli(
        folder=folder,
        public=public_data
    )
    
if __name__ == "__main__":
    gg_id = "1-Dy6xcKH9D5YBeYCav_PZyJwYeZPSnuq"
    data_path = "output"

    print(" Downloading from Google Drive ".center(50, '='))
    download_gg_drive(gg_id, output=data_path)
    print(" Uploading to Kaggle ".center(50, '='))
    upload_kaggle(data_path, "face_occlusion_checkpoint")