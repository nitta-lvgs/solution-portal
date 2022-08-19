# パッケージ・ライブラリをimport
import datetime
import json
import os
import pathlib
import requests
import sys
import time
import traceback
from dotenv import load_dotenv
from http.client import RemoteDisconnected
from os.path import join, dirname
from pathlib import Path
from packaging import version

# 「package」フォルダにあるpyファイルをインポート
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../src/package")

#  pyファイルをインポート
import log
import setting_time
import sheet_api as sa

# .envファイルの内容を読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

def get_eol(technology_name_list):

    # 初期値設定
    today = datetime.date.today()
    eol_output_number = 6
    eol_data_list = [[] for i in range(eol_output_number)]

    # eolを取得する技術名の数だけループする
    for technology_name in technology_name_list:

        try:
            # 技術名のeolを取得
            url = requests.get("https://endoflife.date/api/{}.json".format(technology_name)).text
            data = json.loads(url)

            # 最新のeolを抽出
            eol_data_list[0].append(str(data[0]["cycle"]))
            try: eol_data_list[1].append(data[0]["support"])
            except: eol_data_list[1].append("記載なし")
            try:
                if data[0]["eol"] == False: eol_data_list[2].append("サポート中")
                else: eol_data_list[2].append(data[0]["eol"])
            except: eol_data_list[2].append("記載なし")

            # 期限切れeolを抽出
            for data in data:

                # サポート期限が今日を過ぎているデータの中の最新データを取得
                if str(today) > str(data["eol"]) or data["eol"] == True:
                    eol_data_list[3].append(str(data["cycle"]))
                    try: eol_data_list[4].append(data["support"])
                    except: eol_data_list[4].append("記載なし")
                    try:
                        if data["eol"] == True: eol_data_list[5].append("サポート切れ")
                        else: eol_data_list[5].append(data["eol"])
                    except: eol_data_list[5].append("記載なし")
                    break

            time.sleep(5)

        except RemoteDisconnected:
            print("error!!")

    return eol_data_list

# eol比較関数
def comparison_eol(use_eol_data_list, eol_data_list):

    # 現在使用しているeolと取得したサポート切れのeolを比較
    red_row_list = []
    green_row_list = []
    for count in range(len(use_eol_data_list)):
        if (version.parse(use_eol_data_list[count]) > version.parse(eol_data_list[3][count])) == False:
            red_row_list.append(4 + count)
        else:
            green_row_list.append(4 + count)

    return red_row_list, green_row_list

def main():

    try:

        # eol更新処理開始
        log.action_notice("1", "eol", "【開始】\neol更新を実行します。")
        start_time = time.perf_counter()

        # 対象のスプレッドシート指定
        wks = sa.sheet_data_read(os.environ.get("CLIENT_SECRETS_PATH"), os.environ.get("ON_BOARDING_FOLDER_ID"), os.environ.get("EOL_SHEET_NAME"))

        # オンボにアクセスしeol対象の技術名を取得
        ## H(8)列目の技術名を3行目から取得
        technology_name_list = sa.wks_get_col(wks, 8, 3)
        ## J(10)列目の現在使用しているeolを3行目から取得
        use_eol_data_list = sa.wks_get_col(wks, 10, 3)

        # eol取得
        eol_data_list = get_eol(technology_name_list)

        # オンボ更新
        ## K~P(11~16)列目の3行目から結果を出力
        column_list = [11,12,13,14,15,16]
        sa.wks_update_col(wks, column_list, eol_data_list, 3)

        # eolを比較/整形
        row_list = comparison_eol(use_eol_data_list, eol_data_list)

        # 比較して期限切れのeolがあれば赤色、期限範囲内であれば緑色をセルに塗る
        for row in row_list[0]: sa.wks_fill_cell(wks, (1.0, 0.2, 0), "J", str(row)) # 赤
        for row in row_list[1]: sa.wks_fill_cell(wks, (0, 0.8, 0), "J", str(row)) # 緑

        # 処理時間を取得
        elapsed_time = time.perf_counter() - start_time
        converted_time = setting_time.convert_time(elapsed_time)

        # ログ出力
        log.action_notice("1", "get_eol", "【eol更新完了】")

    except Exception:
        # エラー文整形
        error_message = log.error_log_format(str(traceback.format_exc()))
        log.action_notice("2", "get_eol", error_message)

if __name__ == "__main__":
    main()
