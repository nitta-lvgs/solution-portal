import asana
import datetime
import os
import pathlib
import re
import sys
import time
import traceback
from datetime import date
from dotenv import load_dotenv
from os.path import join, dirname

# 「package」フォルダにあるpyファイルをインポート
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../src/package")

#  pyファイルをインポート
import log

# .envファイルの内容を読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

######################################
#               初期設定               #
######################################

# Asana操作用のクライアント作成
client = asana.Client.access_token(os.environ.get("ASANA_PERSONAL_ACCESS_TOKEN"))

# Slack通知用変数を初期化
sending_count = 0
send_target = []
send_task_name = []

######################################
#           Asana操作用関数            #
######################################

# 指定されたasanaタスク内のサブタスクを全て取得する
def get_subtasks(task_gid):

    result = client.tasks.get_subtasks_for_task(
        task_gid,
        {
            'opt_fields' : [
                'this.name', 'this.due_on',
                'this.assignee',
                'this.assignee.name',
                'completed',
            ],
        },
        opt_pretty=True
    )
    return result

# 指定されたasanaタスク内のストーリー（コメント）を1つだけ作成する
def create_story(task_gid, html_text):

    result = client.stories.create_story_for_task(
        task_gid,
        {
            "html_text": html_text,
            "is_pinned": "false",
        },
        opt_pretty=True
        )
    return result

######################################
#         Asana納品通知処理開始         #
######################################

try:

    # 「【定期実行】一覧」タスクID/サブタスク取得
    subtasks = list(get_subtasks(os.environ.get("ASANA_TARGET_PROJECT_ID")))

    # 今日の日付取得
    today = datetime.date.today()

    # 「【定期実行】一覧」タスク内のサブタスク分処理する
    for subtask in subtasks:

        # 完了していないサブタスクのみ取得
        if subtask["completed"] is False:

            # 完了期限が過ぎているタスクのみ取得
            if str(today) > str(subtask["due_on"]):

                # 今日とタスク期限の日付差分（期限過ぎている日数）を取得
                format_date = datetime.datetime.strptime(subtask["due_on"], '%Y-%m-%d').date()
                elapsed = today - format_date

                # 期限過ぎている日数が2日以下と3日以降でそれぞれ送信文を作成
                if elapsed.days < 3:
                    html_text = "<body>{}さん\nお疲れ様です。納品完了しておりますので、納品確認後にタスク完了をお願いいたします！\n<strong>※タスク完了されていなかった場合、停止させていただくこともありますので、ご確認お願いいたします。</strong></body>".format(subtask["assignee"]["name"])
                elif elapsed.days < 7:
                    html_text = "<body>{}さん\nお疲れ様です。納品完了から{}日経過しておりますが、タスク完了されていません！\n納品確認後にタスク完了をお願いいたします！\n<strong>※明日以降もタスク完了されていない場合、停止させていただくかもしれません。</strong></body>".format(subtask["assignee"]["name"], elapsed.days)
                else:
                    html_text = "<body>{}さん\nお疲れ様です。納品完了から{}日経過しておりますが、タスク完了されていません！\n納品確認後にタスク完了をお願いいたします！\n<strong>※明日以降もタスク完了されていない場合、停止させていただきます。</strong></body>".format(subtask["assignee"]["name"], elapsed.days)

                # タスクのストーリー（コメント）にタスク完了催促文を送信
                stories = list(create_story(subtask["gid"], html_text))

                # slack通知情報収集
                sending_count += 1
                send_target.append(subtask["assignee"]["name"])
                send_task_name.append(subtask["name"])

    # 成功通知
    log.asana_notice("1", "asana_notice", "【asana納品確認通知完了】\n送信件数：{}件\n送信対象者名：{}\n送信タスク名：\n{}\n".format(sending_count, ",".join(send_target), "\n".join(send_task_name))) # 処理成功通知

except:

    # エラー通知
    error_message = log.error_log_format(str(traceback.format_exc()))
    log.asana_notice("2", "asana_notice", error_message)
