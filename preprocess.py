# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/1/5 12:59
# @Author : masai
# @Email : sai.ma@spacexwalk.com
# @File : preprocess.py
# @Software: PyCharm
import json

def process_keystore_migrate():
    with open('./wallet/keystore_migrate.txt','r') as f:
        records = f.read()
        f.close()
    records = records.split('\n')[:-1]
    print(len(records))
    file = open('./wallet/migrated_addresses.txt', 'w')
    for rec in records:
        addr = json.loads(rec)['address']
        file.write(addr+'\n')
        with open('./wallet/0x' + addr + '.keystore', 'w') as f:
            f.write(rec)
            f.close()
    file.close()
    print('done')

if __name__ == '__main__':
    process_keystore_migrate()