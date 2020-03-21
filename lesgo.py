import requests
import pandas as pd
from requests_toolbelt import MultipartEncoder
from tqdm import tqdm
import time
from bs4 import BeautifulSoup


if __name__ == "__main__":
    print('now loading cookies')
    get_cookie = requests.get(
        'http://disperdagin.surabaya.go.id/bahanpokok/tabel')
    # ambil semua nama pasar
    option = BeautifulSoup(get_cookie.content, 'lxml')
    option = option.find_all('option')
    PASARAN = [a['value'] for a in option]
    # ambil cookie buat request
    cookies = get_cookie.cookies.get_dict()
    names = [f'{k}={v};'for k, v in cookies.items()]
    COOKIE = ''.join(names)
    kumpulan_param = []
    dari = input('FROM: YYYY-mm-dd\nCONTOH:2020-03-01\n>')
    sampai = input('TO: YYYY-mm-dd\nCONTOH:2020-03-18\n>')
    print('pastikan tanggal sampai > tanggal')
    for pasar in PASARAN:
        params=MultipartEncoder({
            "JessicaVe48": cookies['ArfNet48'],
            "from-tbl": dari,
            "to-tbl": sampai,
            "psr-tbl": pasar})
        headers = {
            "Host": "disperdagin.surabaya.go.id",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Length": "42",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://disperdagin.surabaya.go.id/bahanpokok/tabel",
            # masalah utama saya, dia gak ngerequests json kayak website biasanya tapi pake this fucking multipar/form-data, jadi harus di "convert" dulu
            "Content-Type": params.content_type,
            "Cookie": COOKIE,
            "DNT": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Origin": "http://disperdagin.surabaya.go.id",
        }
        tot = {
            'name':pasar,
            'param':params,
            'headers':headers
        }
        kumpulan_param.append(tot)
    print("requesting table data")
    for param in tqdm(kumpulan_param):
        start = time.time()
        s = requests.post("http://disperdagin.surabaya.go.id/bahanpokok/tabel",
                        data=param['param'], headers=param['headers'])
        a = s.json()
        df = pd.read_html(a['formtbl'])[0]
        df.to_csv(f'./csv/{param["name"]}.csv', index=False)
