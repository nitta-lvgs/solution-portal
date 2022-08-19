#!/bin/bash

readonly KEY_FILE=bs_server_key_`date "+%Y%m%d"`
### 周期月前の(bs_server_key_[月初の日付])を取得予定
readonly CURRENT_KEY_PATH="/var/python-tool/crawling/tool/key_exchange_tool/current_key/key-test.pem"
readonly CREATE_KEY_PATH="/var/python-tool/crawling/tool/key_exchange_tool/new_key/"
###! ソリューション開発部用のユーザーを作成する予定(ec2-userは削除)
readonly SYSTEM_USER=ec2-user

declare -a OPERATION_SERVER_IP=()
### 管理しているサーバーのIP(csv?やスプレッドシートからIPを配列に格納する予定)
#### memo https://qiita.com/1cco/items/2638a48a2dfb4efac38c
declare -a OPERATION_SERVER_IP=("35.75.19.158") 

# # 鍵作成
ssh-keygen -f ${CREATE_KEY_PATH}${KEY_FILE} -t rsa -N "" 

# 公開鍵をauthorized_keysとしてコピー
cp -ap ${CREATE_KEY_PATH}"${KEY_FILE}.pub" ${CREATE_KEY_PATH}authorized_keys

# SFTPバッチモードで実行テキスト作成
###! ec2-user削除後PATH変更
echo "cd /home/ec2-user/.ssh \nchmod 600 authorized_keys \nquit" > SFTP_COMMANDS.txt

# 秘密鍵の権限の変更
chmod 400 ${CREATE_KEY_PATH}${KEY_FILE}

# IPの配列分foreach
for IP in "${OPERATION_SERVER_IP[@]}"
do
    echo "${IP}"
    ## authorized_keysのバックアップはいらない？

    ## ローカルのauthorized_keysをサーバーのauthorized_keysに上書き
    scp -i ${CURRENT_KEY_PATH} ${CREATE_KEY_PATH}authorized_keys ${SYSTEM_USER}@${IP}:/home/ec2-user/.ssh
    ## authorized_keysの権限を600に変更
    sftp -i ${CREATE_KEY_PATH}${KEY_FILE} -b SFTP_COMMANDS.txt ${SYSTEM_USER}@${IP}
done

## 鍵ファイルをgoogleDriveにアップロード

export CLIENT_ID=692953111369-8n2tcdeo54l1aihkgooki9v0h6lkqs8h.apps.googleusercontent.com
export CLIENT_SECRET="Fy-XJQ1Wf02tvf3vUZ7GX1pl"
export REDIRECT_URI=urn:ietf:wg:oauth:2.0:oob
export SCOPE=https://www.googleapis.com/auth/drive

## コード発行
# echo "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URI&scope=$SCOPE&access_type=offline"
# export AUTHORIZATION_CODE="4/1AX4XfWhB8VsYkR_G0oZZtCFiLGhn1wp-mkWwJqZyfQmha-H3VFTqIwaZhrU"

## リフレッシュトークン発行
# curl \
#   --data "code=$AUTHORIZATION_CODE" \
#   --data "client_id=$CLIENT_ID" \
#   --data "client_secret=$CLIENT_SECRET" \
#   --data "redirect_uri=$REDIRECT_URI" \
#   --data "grant_type=authorization_code" \
#   --data "access_type=offline" \
#   https://www.googleapis.com/oauth2/v4/token -s

export REFRESH_TOKEN="1//0e1TbrtO3xfWECgYIARAAGA4SNwF-L9Iriwm9eHphUAS5ykzvAza-g9_yfVoHH_lncFD4HC9a5zGJn0lH5AzqhOWlL1N4N8KY3zE"
export ACCESS_TOKEN=`curl --data "refresh_token=$REFRESH_TOKEN" --data "client_id=$CLIENT_ID" --data "client_secret=$CLIENT_SECRET" --data "grant_type=refresh_token" https://www.googleapis.com/oauth2/v4/token -s | jq  -r .access_token`

curl -X POST \
 -H "Authorization: Bearer $ACCESS_TOKEN" \
 -F "metadata={ \
              name : '${KEY_FILE}', \
              mimeType : 'text/plain', \
              parents: ['10bJ8Jpg6bW5vT11C059fTNDLarOyf1sN'] \
              };type=application/json;charset=UTF-8" \
 -F "file=@${CREATE_KEY_PATH}${KEY_FILE};type=text/plain" \
 "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
