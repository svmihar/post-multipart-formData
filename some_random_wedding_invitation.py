# wah kebetulan dapet nya ini wah

import requests
from requests_toolbelt import MultipartEncoder
from tqdm import tqdm
import uuid
import time
from bs4 import BeautifulSoup


URL = 'https://www.syifadwiky-wedding.com/'

def get_params(nama, ucapan):
    hasil = {
        'nama': nama,
        'status': 'Y',
        'ucapan':ucapan,
        'simpan': 'S U B M I T'
    }
    return MultipartEncoder(hasil)

def main():
    s = requests.post(URL, data=get_params(str(uuid.uuid4()), str(uuid.uuid4())))
    return s
if __name__ == "__main__":
    for _ in tqdm(range(10000)):
        s = main()
        if s.status_code == 200:
            pass
        else:
            print('error')
