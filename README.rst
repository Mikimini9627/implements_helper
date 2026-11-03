=====================
implements_helper
=====================

Python 実装時に利用できるユーティリティ群です。

----------------
インストール方法
----------------

.. code-block:: console

    $ pip install implements_helper

--------
使用方法
--------

.. code-block:: python

    import implements_helper

    # 日本時間のタイムスタンプ付きでログ出力
    implements_helper.print_log("処理開始")
    # => 2026/11/03 12:34:56 処理開始

    # リストを 3 分割 (各ブロックの要素数の差は 1 以下)
    implements_helper.split_list([1, 2, 3, 4, 5, 6, 7], 3)
    # => [[1, 2, 3], [4, 5], [6, 7]]

    # 疎通確認済みのプロキシリスト取得 (失敗時は空リスト)
    proxy_list = implements_helper.get_proxy_list()

    # 有効なプロキシを 1 つだけ取得
    proxy_list = implements_helper.get_proxy_list(get_only_one=True)

--------
必要要件
--------
* Python >=3.12
* requests >=2.32.3,<3.0.0
* beautifulsoup4 >=4.12.0,<5.0.0
* lxml >=5.3.0,<7.0.0
* useragent-changer >=0.3.2,<0.4.0
