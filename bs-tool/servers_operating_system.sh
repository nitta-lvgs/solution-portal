#!/bin/bash

source ./.env

declare -a ec2_id_list=()
declare -a ec2_id_list=($SCOUT_EC2_ID $PROD_VOICE_EC2_ID)
declare -a ec2_name_list=()
declare -a ec2_name_list=($SCOUT_ACCOUNT $PROD_VOICE_ACCOUNT)

readonly LOG_FILE_PATH="$LOG_SETTING_PATH$(basename $0 .sh)_$(date '+%Y%m%d').log"

output_log () {
    local readonly LOCAL_LOG_MESSAGE=$1
    echo "[$(date '+%Y/%m/%d %H:%M:%S')] [$(basename $0)] ${LOCAL_LOG_MESSAGE}" | tee -a ${LOG_FILE_PATH}
}

for ((i = 0; i < ${#ec2_id_list[@]}; i++))

do
    INSTANCE_STATUS=`aws ec2 describe-instance-status --instance-ids "${ec2_id_list[$i]}" --profile ${ec2_name_list[$i]} | jq -r '.InstanceStatuses[].InstanceState.Name'`

    ## 指定EC2インスタンスの起動(aws ec2 start-instances).
    if [ -n "$1" ] && [ $1 = '--start' ] ; then

        if [ -n "$INSTANCE_STATUS" ] && [ $INSTANCE_STATUS = 'running' ] ; then
            ## 稼働中なら何もしない
            output_log "${ec2_name_list[$i]}　status is running. nothing to do."
        else
            ## 停止中なら起動
            output_log "${ec2_name_list[$i]} status is stopped."
            aws ec2 start-instances --instance-ids "${ec2_id_list[$i]}" --profile ${ec2_name_list[$i]}
            output_log "${ec2_name_list[$i]}　instance starting..."
        fi

    ## 指定EC2インスタンスの停止(stop). 
    elif [ -n "$1" ] && [ $1 = '--stop' ] ; then

        if [ -n "$INSTANCE_STATUS" ] && [ $INSTANCE_STATUS = 'running' ] ; then
            ## 稼働中なら停止
            output_log "${ec2_name_list[$i]} status is running."
            aws ec2 stop-instances --instance-ids "${ec2_id_list[$i]}" --profile ${ec2_name_list[$i]}
            output_log "${ec2_name_list[$i]}　instance stopping..."
        else
            ## 停止中なら何もしない
            output_log "${ec2_name_list[$i]} status is stopped. nothing to do."
        fi
    fi
done
