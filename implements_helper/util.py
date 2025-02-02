import math
import traceback
import datetime
import requests
import bs4
from useragent_changer import UserAgent

def print_log(text):
    print(str(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=9).strftime('%Y/%m/%d %H:%M:%S')) + " " + text)

def split_list(target, split_count):

    try:
        # 1ブロックのサイズを計算する
        one_block_count = math.ceil(len(target) / split_count)

        # 分割したリストを返却する
        return [target[index: index + one_block_count] for index in range(0, len(target), one_block_count)]
    except Exception:
        print_log(traceback.format_exc())
        return None

def get_proxy_list(is_first : bool = False) -> list:

    #Free Proxy Listサイト情報取得
    res = requests.get('https://free-proxy-list.net/')

    bs_data = bs4.BeautifulSoup(res.text, features="lxml")

    # tbody要素取得
    tbody_data = bs_data.find("tbody")

    # tr要素取得
    tr_data = tbody_data.find_all("tr")

    ip_list = []
    for tr in tr_data:

        # td要素取得
        td_data = tr.find_all("td")

        # コード
        td_data[2].text

        # IPアドレス
        ip = td_data[0].text

        # ポート番号
        port = td_data[1].text

        try:
            requests.get('https://api.ipify.org?format=json', proxies = {'http': 'http://' + ip + ":" + port,
                'https': 'http://' + ip + ":" + port}, headers = {'User-Agent': UserAgent('chrome').set()}, timeout = 1)
        except Exception:
            continue

        # リストに追加
        ip_list.append('http://' + ip + ":" + port)

        if is_first == True:
            break

    return ip_list