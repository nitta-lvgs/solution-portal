import asyncio
import boto3
import os
import pathlib
import sys
import traceback
from dotenv import load_dotenv
from os.path import join, dirname

# 「package」フォルダにあるpyファイルをインポート
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../src/package")

#  pyファイルをインポート
import log
import sheet_api as sa

# .envファイルの内容を読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# スプレッドシート書き込み関数
def wks_write_value(elastic_ip):

    # 対象のスプレッドシート指定
    wks = sa.sheet_data_read(os.environ.get("CLIENT_SECRETS_PATH"), os.environ.get("CRAWLING_FOLDER_ID"), os.environ.get("CRAWLING_SHEET_NAME"))

    # スプレッドシートにIP書き込み
    sa.wks_update_value(wks, "D4", elastic_ip)

async def main():

    try:

        # EIP取得処理
        ec2 = boto3.client('ec2',
                            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                            )
        filters = [
        {'Name': 'instance-id', 'Values': [os.environ.get("CRAWLING_INSTANCE_ID")]}
        ] # EC2のインスタンスIDでフィルターする
        addresses = ec2.describe_addresses(Filters=filters)
        address_list = addresses["Addresses"]
        primary_ip = address_list[0] if len(address_list) else ''
        old_allocationid = primary_ip["AllocationId"]
        allocation = ec2.allocate_address(Domain='vpc') # EIP取得
        associate = ec2.associate_address(AllocationId=allocation['AllocationId'],InstanceId=os.environ.get("CRAWLING_INSTANCE_ID")) # EIP関連付け
        release = ec2.release_address(AllocationId=old_allocationid) # 古いEIPを開放

        # IP切り替えログを出力
        log.action_notice("1", "elasticip_switch", "【IP切り替え完了】\nElasticIP： {0}".format(allocation["PublicIp"]))

        # スプレッドシート書き込み
        loop = asyncio.get_running_loop()
        await asyncio.wait_for(
            loop.run_in_executor(None, wks_write_value, allocation["PublicIp"]),
            timeout=10 # 10秒経ったら強制タイムアウト
        )

        # 完了ログを出力
        log.action_notice("1", "elasticip_switch", "【SS書き込み完了】")

    # スプレッドシート取得エラー
    except asyncio.TimeoutError:

        # 失敗通知
        log.action_notice("2", "elasticip_switch", "【エラー】\nasyncio.TimeoutError\nSS書き込み失敗")

    # その他エラー
    except:

        # エラー文整形
        error_message = log.error_log_format(str(traceback.format_exc()))
        log.action_notice("2", "elasticip_switch", "【エラー】\n" + error_message)

if __name__ == "__main__":
    asyncio.run(main())
