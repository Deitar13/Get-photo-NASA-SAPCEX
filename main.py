import requests
import json
import os
import os.path
import datetime

from pathlib import Path
from urllib.parse import urlsplit
from urllib.parse import urlparse
from dotenv import load_dotenv




def get_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1]


def fetch_apod_photos(nasa_url):
    count = 30
    payload = {"api_key": f"{NASA_API_TOKEN}", "count": f"{count}"}
    response = requests.get(nasa_url, params=payload)
    response.raise_for_status()

    file_path = "apod_images"
    ensure_dir(file_path)

    urls_count = 0
    for item in response.json():
        parsed_url = urlparse(item['url'])
        if parsed_url.netloc == "apod.nasa.gov":
            urls_count += 1
            extension = get_extension(item['url'])
            photo_name = (f"apod{urls_count}{extension}")
            response = requests.get(item['url'])
            response.raise_for_status
            with open(f"{file_path}/{photo_name}", 'wb') as file:
                file.write(response.content)


def ensure_dir(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)


def fetch_spacex_last_launch(url, file_path):
    links_list = []
    response = requests.get(url)
    response.raise_for_status

    for item in response.json():
        if item["links"]["flickr_images"] != []:
            links_list.append(item["links"]["flickr_images"])
    last_photos_links = links_list[-1]

    for photo_number, link in enumerate(last_photos_links, 1):
        image_name = (f"spacex{photo_number}.jpg")
        response = requests.get(link)
        response.raise_for_status
        with open(f"{file_path}/{image_name}", 'wb') as file:
            file.write(response.content)


def get_epic_earth_photos_urls(epic_url):
    response = requests.get(epic_url)
    response.raise_for_status()

    for photo_info in response.json():
        name_of_photo = photo_info["image"]
        date_of_photo = datetime.datetime.fromisoformat(photo_info["date"])
        formatted_date_of_photo = date_of_photo.strftime("%Y/%m/%d")
        epic_earth_photo_url = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date_of_photo}/png/{name_of_photo}.png?api_key=DEMO_KEY'
        download_epic_earth_photo(epic_earth_photo_url, name_of_photo)


def download_epic_earth_photo(epic_earth_photo_url, name_of_photo):
    file_path = "epic_earth_photo"
    ensure_dir(file_path)
    response = requests.get(epic_earth_photo_url)
    response.raise_for_status
    with open(f"{file_path}/{name_of_photo}.png", 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":

    load_dotenv()
    NASA_API_TOKEN = os.environ["NASA_API_TOKEN"]

    file_path = "images"
    ensure_dir(file_path)

    url = 'https://api.spacexdata.com/v3/launches/'

    fetch_spacex_last_launch(url, file_path)

    nasa_url = "https://api.nasa.gov/planetary/apod"
    fetch_apod_photos(nasa_url)

    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images?api_key=DEMO_KEY'
    get_epic_earth_photos_urls(epic_url)
