import subprocess
import re
import os
import socket
from os.path import join, dirname
from dotenv import load_dotenv
from itertools import chain

# .envファイルの内容を読み込みます
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_ec2_ip(id, account):
    get_ip = (subprocess.run("aws ec2 describe-instances --filters 'Name=instance-id,Values=\"{}\"' --query 'Reservations[].Instances[].PublicIpAddress' --output text --profile {}".format(id, account), shell=True, stdout=subprocess.PIPE, encoding='UTF-8'))
    ec2_ip = re.sub("\r|\t|\n|\u3000|\xa0| ","", get_ip.stdout)
    
    return ec2_ip


def server_template_toml(ec2_media, ec2_ip):
    toml_create_list = []
    server_name = ['[servers.{}]\n'.format(ec2_media)]
    server_host = ['host = "{}"\n'.format(ec2_ip)]
    server_port = ['port = "22"\n']
    server_user = ['user = "bs-admin"\n']
    server_keypath = ['keyPath = "/root/.ssh/bs_server_key_20220513"\n']
    server_configpath = ['sshConfigPath = "/root/.ssh/config"\n\n']
    toml_create_list += [server_name, server_host, server_port, server_user,  server_keypath, server_configpath]
    
    return toml_create_list


crawling_ip = get_ec2_ip(os.environ.get("CRAWLING_EC2_ID"), os.environ.get("CRAWLING_ACCOUNT"))
scount_ip = get_ec2_ip(os.environ.get("SCOUT_EC2_ID"), os.environ.get("SCOUT_ACCOUNT"))
prod_voice_ip = get_ec2_ip(os.environ.get("PROD_VOICE_EC2_ID"), os.environ.get("PROD_VOICE_ACCOUNT"))
prod_ma_ip = get_ec2_ip(os.environ.get("PROD_MA_EC2_ID"), os.environ.get("MA_EC2_ACCOUNT"))
stg_ma_ip = get_ec2_ip(os.environ.get("STG_MA_EC2_ID"), os.environ.get("MA_EC2_ACCOUNT"))
prod_leve_ip = get_ec2_ip(os.environ.get("PROD_LEVE_EC2_ID"), os.environ.get("PROD_LEVE_EC2_ACCOUNT"))
stg_leve_ip = get_ec2_ip(os.environ.get("STG_LEVE_EC2_ID"), os.environ.get("STG_LEVE_EC2_ACCOUNT"))
prod_hrd_ip = get_ec2_ip(os.environ.get("PROD_HRD_EC2_ID"), os.environ.get("HRD_EC2_ACCOUNT"))
stg_hrd_ip = get_ec2_ip(os.environ.get("STG_HRD_EC2_ID"), os.environ.get("HRD_EC2_ACCOUNT"))

ec2_name_list = [

            'inspection-server',
            'crawling-server',
            'scount-server',
            'prod-voice-transcription',
            'prod-ma-corp-server',
            'stg-ma-corp-server',
            'prod-leverages-corp-server',
            'stg-leverages-corp-server',
            'prod-hrd-corp-server',
            'stg-hrd-corp-server',

            ]

ec2_ip_list = [

            '{}'.format(socket.gethostbyname(socket.gethostname())),
            '{}'.format(crawling_ip),
            '{}'.format(scount_ip),
            '{}'.format(prod_voice_ip),
            '{}'.format(prod_ma_ip),
            '{}'.format(stg_ma_ip),
            '{}'.format(prod_leve_ip),
            '{}'.format(stg_leve_ip),
            '{}'.format(prod_hrd_ip),
            '{}'.format(stg_hrd_ip),

            ]

template_list = [

            '[slack]\n',
            'hookURL = "{}"\n'.format(os.environ.get("WEB_HOOK_URL")),
            'channel = "{}"\n'.format(os.environ.get("POST_SLACK_CHANNEL")),
            'authUser = "{}"\n\n'.format(os.environ.get("POST_SLACK_USER")),
            '[servers] \n\n',

            ]

f = open('/home/bs-admin/vulsctl/docker/config.toml', 'w')

toml_create_list = []

count = 0

for i in ec2_name_list:
    server_data = server_template_toml(i, ec2_ip_list[count])
    
    count += 1
    
    for i in range(6):
        toml_create_list.append(server_data[i][0])

toml_list = list(chain(template_list, toml_create_list))

f.writelines(toml_list)

f.close()
