import datetime
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import bs4
import requests
from useragent_changer import UserAgent

__all__ = ["print_log", "split_list", "get_proxy_list"]

# 日本標準時
JST = datetime.timezone(datetime.timedelta(hours=9), "JST")

# プロキシ一覧の取得元
PROXY_LIST_URL = "https://free-proxy-list.net/"

# プロキシの疎通確認先
PROXY_CHECK_URL = "https://api.ipify.org?format=json"

def print_log(text : str) -> None:
    '''概要

    yyyy/MM/dd HH:mm:ss 形式のタイムスタンプ(日本時間)を伴って出力する

    Parameters
    ----------
        text : str
            出力するログメッセージ

    Returns
    -------
        なし
    '''

    # yyyy/MM/dd HH:mm:ss 形式のタイムスタンプを伴って出力
    print(datetime.datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S') + " " + str(text))

def split_list(target : list, split_count : int) -> list:
    '''概要

    指定したリストを指定した分割数で、各ブロックの要素数の差が 1 以下になるよう分割し返す
    要素数が分割数より少ない場合は、要素数と同じ数のブロックに分割する

    Parameters
    ----------
        target : list
            対象とするリスト
        split_count : int
            分割数 (1 以上)

    Returns
    -------
        split_list : list
            分割したリスト

    Raises
    ------
        ValueError
            split_count が 1 未満の場合
    '''

    # 分割数が正の整数でない場合はエラーとする
    if split_count <= 0:
        raise ValueError("split_count は 1 以上を指定してください")

    # 実際のブロック数(空のブロックは作らない)
    block_count = min(split_count, len(target))
    if block_count == 0:
        return []

    # 基本のブロックサイズと、1 要素多く持つブロックの数を計算する
    base_size, remainder = divmod(len(target), block_count)

    result = []
    start = 0
    for index in range(block_count):
        end = start + base_size + (1 if index < remainder else 0)
        result.append(target[start:end])
        start = end

    return result

def _check_proxy(proxy : str, user_agent : str, timeout : float) -> bool:
    '''概要

    指定したプロキシ経由で疎通確認先にアクセスできるか確認する

    Parameters
    ----------
        proxy : str
            確認するプロキシ (http://IP:PORT 形式)
        user_agent : str
            リクエストに使用する User-Agent
        timeout : float
            タイムアウト秒数

    Returns
    -------
        result : bool
            アクセスできた場合 True
    '''

    try:
        response = requests.get(PROXY_CHECK_URL, proxies = {'http': proxy, 'https': proxy},
            headers = {'User-Agent': user_agent}, timeout = timeout)
        return response.ok
    except requests.RequestException:
        return False

def get_proxy_list(get_only_one : bool = False, timeout : float = 1, max_workers : int = 32) -> list:
    '''概要

    https://free-proxy-list.net/ から有効なプロキシリストを取得する

    Parameters
    ----------
        get_only_one : bool
            1つのプロキシのみを取得するかどうか
            デフォルト : False
        timeout : float
            各プロキシの疎通確認のタイムアウト秒数
            デフォルト : 1
        max_workers : int
            疎通確認を並列に行うスレッド数
            デフォルト : 32

    Returns
    -------
        proxy_list : list
            取得したプロキシリスト (http://IP:PORT 形式)
            取得に失敗した場合は空のリスト
    '''

    proxy_list = []

    try:
        user_agent = UserAgent('chrome').set()

        # Free Proxy Listサイト情報取得
        html_source = requests.get(PROXY_LIST_URL, headers = {'User-Agent': user_agent}, timeout = 10)
        html_source.raise_for_status()

        # Beautiful soupでパース
        bs_data = bs4.BeautifulSoup(html_source.text, features = "lxml")

        # tbody要素取得
        tbody_data = bs_data.find("tbody")
        if tbody_data is None:
            raise ValueError("プロキシ一覧のテーブルが見つかりません")

        # 候補となるプロキシを抽出
        candidates = []
        for tr in tbody_data.find_all("tr"):

            # td要素取得
            td_data = tr.find_all("td")
            if len(td_data) < 2:
                continue

            # IPアドレス、ポート番号
            ip = td_data[0].text.strip()
            port = td_data[1].text.strip()

            candidates.append('http://' + ip + ":" + port)

    except Exception:
        print_log(traceback.format_exc())
        return proxy_list

    # 疎通確認を並列で実施する
    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        futures = {executor.submit(_check_proxy, proxy, user_agent, timeout): proxy for proxy in candidates}

        for future in as_completed(futures):
            if not future.result():
                continue

            # リストに追加
            proxy_list.append(futures[future])

            if get_only_one:
                # 未実行の確認はキャンセルする
                executor.shutdown(wait = False, cancel_futures = True)
                break

    # 取得元サイトの掲載順に並べ直す
    proxy_list.sort(key = candidates.index)

    return proxy_list
