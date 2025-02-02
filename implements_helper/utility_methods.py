import math
import traceback
import datetime
import requests
import bs4
from useragent_changer import UserAgent

def print_log(text : str) -> None:
    '''概要

    yyyy/MM/dd HH:mm:ss 形式のタイムスタンプを伴って出力する

    Parameters
    ----------
        text : str
            出力するログメッセージ

    Returns
    -------
        なし
    '''

    # yyyy/MM/dd HH:mm:ss 形式のタイムスタンプを伴って出力
    print(str((datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')) + " " + text)

def split_list(target : list, split_count : int) -> list:
    '''概要

    指定したリストを指定した分割数で分割し返す

    Parameters
    ----------
        target : list
            対象とするリスト
        split_count : int
            分割数

    Returns
    -------
        split_list : list
            分割したリスト
    '''

    split_list = None

    try:
        # 1ブロックのサイズを計算する
        one_block_count = math.ceil(len(target) / split_count)

        # 分割したリストを返却する
        split_list = [target[index: index + one_block_count] for index in range(0, len(target), one_block_count)]

    except Exception:
        print_log(traceback.format_exc())
    
    finally:
        return split_list

def get_proxy_list(get_only_one : bool = False) -> list:
    '''概要

    https://free-proxy-list.net/ から有効なプロキシリストを取得する

    Parameters
    ----------
        get_only_one : bool
            1つのプロキシのみを取得するかどうか
            デフォルト : False

    Returns
    -------
        proxy_list : list
            取得したプロキシリスト
    '''

    proxy_list = None

    try:
        
        # Free Proxy Listサイト情報取得
        html_source = requests.get('https://free-proxy-list.net/')

        # Beautiful soupでパース
        bs_data = bs4.BeautifulSoup(html_source.text, features = "lxml")

        # tbody要素取得
        tbody_data = bs_data.find("tbody")

        # tr要素取得
        tr_data = tbody_data.find_all("tr")

        proxy_list = []
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
            proxy_list.append('http://' + ip + ":" + port)

            if get_only_one is True:
                break
    
    except Exception:
        print_log(traceback.format_exc())

    finally:
        return proxy_list