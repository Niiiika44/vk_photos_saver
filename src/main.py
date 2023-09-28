import json
import re
import requests

VK_USER_ID = 
VK_TOKEN = ""


def load_url(url, name, directory='saved', data_format='png'):
    response = requests.get(url, timeout=10)
    with open(f"{directory}/{name}.{data_format}", "wb") as f:
        f.write(response.content)


def get_photo_data(offset=0, count=2):
    api = requests.get("https://api.vk.com/method/photos.getAll",
                       params={
                           'owner_id': VK_USER_ID,
                           'access_token': VK_TOKEN,
                           'offset': offset,
                           'count': count,
                           'photo_sizes': 0,
                           'v': 5.103},
                           timeout=1)
    return json.loads(api.text)


def get_album_ids():
    dct_album_id = {}
    response = requests.get("https://api.vk.com/method/photos.getAlbums",
                     params={
                         'access_token': VK_TOKEN,
                         'v': '5.150 (текущая)'},
                         timeout=2)
    json_ans = json.loads(response.text)
    for item in json_ans["response"]["items"]:
        name_album = item["title"]
        id_album = item["id"]
        dct_album_id[name_album] = id_album
    return dct_album_id


def get_album_id_by_name(album_name):
    dct_id = get_album_ids()
    regex = rf'{album_name}*'
    for k, v in dct_id.items():
        if re.search(regex, k, flags=re.I):
            return v
    return None


def get_photos_count_from_album(id_album):
    response = requests.get("https://api.vk.com/method/photos.get",
                            params={
                                'access_token': VK_TOKEN,
                                'album_id': id_album,
                                'rev': 0,
                                'v': '5.150 (текущая)'},
                                timeout=2)
    json_ans = json.loads(response.text)
    count = int(json_ans["response"]["count"])
    return count


def get_photos_from_album(id_album, offset, count):
    response = requests.get("https://api.vk.com/method/photos.get",
                            params={
                                'access_token': VK_TOKEN,
                                'album_id': id_album,
                                'rev': 0,
                                'offset': offset,
                                'count': count,
                                'v': '5.150 (текущая)'},
                                timeout=2)
    json_ans = json.loads(response.text)
    for pic in json_ans["response"]["items"]:
        url = pic["sizes"][-1]["url"]
        filename = hash(url)
        load_url(url, filename)


if __name__ == "__main__":
#    data = get_photo_data()
#    i = 0
#    for file in data["response"]["items"]:
#        url = file["sizes"][-1]["url"]
#        load_url(url, i)
#        i += 1
    
    get_photos_from_album(254685021, 0, 105)
