# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/10 10:12
# @Author : masai
# @File : main.py
# @Software: PyCharm
import copy
import json
import time
import sys
import traceback
import logging
import requests
import eth_api
from flask import Flask, request

app = Flask(__name__)
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter

logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(filename='./logs/logfile.log', when='D',
                                   interval=1, backupCount=1, encoding='utf-8', delay=False)
formatter = Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
print('Web3 Service Started.')

apikey_alchemy = ''
apikey_moralis = ''
proxies = {'http': None, 'https': None}
response_template = {
    "state": 200,
    "msg": "Successful",
    "body": {}
}

# 生成TRC20/ERC20地址
@app.route('/creation/address/erc20', methods=['POST'])
def creationAddress():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    print('Create ERC20 new address.')
    try:
        address = eth_api.createAccount()
        json_response['body']['address'] = address
        json_response['body']['status'] = 'NEW'
        print(json_response)
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


# 获取一个地址账户信息
@app.route('/account/erc20', methods=['GET'])
def getAccount():  # 查询本币余额
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    address = args.get('address')
    chain = args.get('chain', default='eth')
    # print('aaa', address, chain)
    if address is None:
        print('Address should not be null.')
        json_response['msg'] = 'Address should not be null.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)
    try:
        balance = eth_api.getBalance(address, chain)
        json_response['body']['balance'] = str(balance)
        json_response['body']['address'] = address
        json_response['body']['id'] = ''
        json_response['body']['name'] = ''
        json_response['body']['createTime'] = ''
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/contract/erc20/<symbolOrAddr>', methods=['GET'])
def getContract(symbolOrAddr):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    from_address = args.get('from')
    chain = args.get('chain', default='eth')
    if symbolOrAddr is None:
        print('symbolOrAddr should not be null.')
        json_response['msg'] = 'symbolOrAddr should not be null.'
        return json.dumps(json_response)
    try:
        name, symbol, decimals, totalSupply = \
            eth_api.tokenContractInfo(symbolOrAddr, chain)
        totalSupply /= 10 ** decimals
        json_response['body']['totalSupply'] = totalSupply
        json_response['body']['decimals'] = decimals
        json_response['body']['symbol'] = symbol
        json_response['body']['name'] = name
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)

# 获取一个地址的ERC20代币余额
@app.route('/balance/erc20', methods=['GET'])
def balanceOf():  # 查询代币余额，本币余额用getAccount方法
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    address = args.get('address')
    symbolOrAddr = args.get('symbolOrAddr')
    chain = args.get('chain', default='eth')
    # print('aaa', address, chain)
    if (address is None) or (symbolOrAddr is None):
        print('Address/symbolOrAddr should not be null.')
        json_response['msg'] = 'Address/symbolOrAddr should not be null.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    try:
        balance = eth_api.getBalanceByToken(address, symbolOrAddr, chain)
        json_response['body']['balance'] = str(balance)
        json_response['body']['address'] = address
        json_response['body']['symbolOrAddr'] = symbolOrAddr
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/decimals/erc20/<symbolOrAddr>', methods=['GET'])
def getDecimals(symbolOrAddr):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    owner = args.get('owner')
    chain = args.get('chain', default='eth')
    if symbolOrAddr is None:
        print('Address/symbolOrAddr should not be null.')
        json_response['msg'] = 'Address/symbolOrAddr should not be null.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    try:
        name, symbol, decimals, totalSupply = \
            eth_api.tokenContractInfo(symbolOrAddr, chain)
        json_response['body']['decimals'] = int(decimals)
        json_response['body']['symbolOrAddr'] = symbolOrAddr
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/transfer/eth', methods=['POST'])
def transferETH():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    from_address = args.get('from')
    to_address = args.get('to')
    amount = args.get('amount')
    param = args.get('param')
    chain = args.get('chain', default='eth')
    if (to_address is None) or (from_address is None):
        print('From address/To address should not be null.')
        json_response['msg'] = 'From address/To address should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) <= 0):
        print('The transfer amount must be greater than 0.')
        json_response['msg'] = 'The transfer amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    try:
        txHash = eth_api.sendTransaction(send_from=from_address, value=amount,
                                         send_to=to_address, chain=chain)
        # print('Tx hash got.')
        json_response['body']['resultHash'] = txHash
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)

@app.route('/transfer/erc20', methods=['POST'])
def transfer():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    from_address = args.get('from')
    to_address = args.get('to')
    amount = args.get('amount')
    symbolOrAddr = args.get('symbolOrAddr')
    memo = args.get('memo')
    chain = args.get('chain', default='eth')
    if (to_address is None) or (from_address is None):
        print('From address/To address should not be null.')
        json_response['msg'] = 'From address/To address should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) <= 0):
        print('The transfer amount must be greater than 0.')
        json_response['msg'] = 'The transfer amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)
    name, symbol, decimals, totalSupply = \
        eth_api.tokenContractInfo(symbolOrAddr, chain)
    amount = float(amount) * (10 ** int(decimals))
    try:
        txHash = eth_api.callERC20('transfer', from_address, to_address, \
                                   amount, symbolOrAddr, chain)
        json_response['body']['resultHash'] = txHash
        json_response['body']['status'] = 'SUCCESS'
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/transferFrom/erc20', methods=['POST'])
def transferFrom():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    from_address = args.get('from')
    to_address = args.get('to')
    spender = args.get('spender')
    amount = args.get('amount')
    symbolOrAddr = args.get('symbolOrAddr')
    memo = args.get('memo')
    chain = args.get('chain', default='eth')
    if (to_address is None) or (from_address is None):
        print('From address/To address should not be null.')
        json_response['msg'] = 'From address/To address should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) <= 0):
        print('The transfer amount must be greater than 0.')
        json_response['msg'] = 'The transfer amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)
    name, symbol, decimals, totalSupply = \
        eth_api.tokenContractInfo(symbolOrAddr, chain)
    amount = float(amount) * (10 ** int(decimals))
    try:
        txHash = eth_api.callERC20('transferFrom', from_address, to_address, \
                                   amount, symbolOrAddr, chain, spender=spender)
        json_response['body']['status'] = 'SUCCESS'
        json_response['body']['resultHash'] = txHash
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/deploy/<chain>/erc20', methods=['POST'])
def deploy(chain):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    owner = args.get('owner')
    name = args.get('name')
    symbol = args.get('symbol')
    decimals = int(args.get('decimals'))
    totalSupply = args.get('totalSupply')
    if (owner is None):
        print('Owner address should not be null.')
        json_response['msg'] = 'Owner address should not be null.'
        return json.dumps(json_response)
    if (symbol is None) or (name is None):
        print('Symbol/Name should not be null.')
        json_response['msg'] = 'Symbol/Name should not be null.'
        return json.dumps(json_response)
    if (int(decimals) is None) or (int(decimals) < 0) or (int(decimals) > 20):
        print('Decimals are numbers and range from 1-20.')
        json_response['msg'] = 'Decimals are numbers and range from 1-20.'
        return json.dumps(json_response)
    if (totalSupply is None) or (float(totalSupply) <= 0):
        print('Total supply must be greater than 0.')
        json_response['msg'] = 'Total supply must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    try:
        txHash, contract_addr = eth_api.deployERC20(owner, name, symbol,
                                    int(totalSupply), decimals, chain)
        json_response['body']['resultHash'] = txHash
        json_response['body']['status'] = 'SUCCESS'
        json_response['body']['content'] = contract_addr
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/mint/<chain>/erc20/<symbolOrAddr>', methods=['POST'])
def mint(chain, symbolOrAddr):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    owner = args.get('owner')
    amount = args.get('amount')
    if (owner is None):
        print('Owner address should not be null.')
        json_response['msg'] = 'Owner address should not be null.'
        return json.dumps(json_response)
    if (symbolOrAddr is None):
        print('Symbol/Address should not be null.')
        json_response['msg'] = 'Symbol/Address should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) <= 0):
        print('Mint amount must be greater than 0.')
        json_response['msg'] = 'Mint amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)
    name, symbol, decimals, totalSupply = \
        eth_api.tokenContractInfo(symbolOrAddr, chain)
    amount = float(amount) * (10 ** int(decimals))
    try:
        txHash = eth_api.callERC20('mint', owner, '', amount, symbolOrAddr, chain)
        json_response['body']['resultHash'] = txHash
        json_response['body']['status'] = 'SUCCESS'
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/burn/<chain>/erc20/<symbolOrAddr>', methods=['POST'])
def burn(chain, symbolOrAddr):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    owner = args.get('owner')
    amount = args.get('amount')
    if (owner is None):
        print('Owner address should not be null.')
        json_response['msg'] = 'Owner address should not be null.'
        return json.dumps(json_response)
    if (symbolOrAddr is None):
        print('Symbol/Address should not be null.')
        json_response['msg'] = 'Symbol/Address should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) <= 0):
        print('Burn amount must be greater than 0.')
        json_response['msg'] = 'Burn amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    name, symbol, decimals, totalSupply = \
        eth_api.tokenContractInfo(symbolOrAddr, chain)
    amount = float(amount) * (10 ** int(decimals))
    try:
        txHash = eth_api.callERC20('burn', owner, '', amount, symbolOrAddr, chain)
        json_response['body']['resultHash'] = txHash
        json_response['body']['status'] = 'SUCCESS'
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/approve/erc20', methods=['POST'])
def approve():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    owner = args.get('owner')
    spender = args.get('spender')
    symbolOrAddr = args.get('symbolOrAddr')
    creditLine = args.get('creditLine')
    # memo = args.get('memo')
    # param = args.get('param')
    chain = args.get('chain')

    if (owner is None):
        print('Owner address should not be null.')
        json_response['msg'] = 'Owner address should not be null.'
        return json.dumps(json_response)
    if (symbolOrAddr is None):
        print('Symbol/Address should not be null.')
        json_response['msg'] = 'Symbol/Address should not be null.'
        return json.dumps(json_response)
    if (creditLine is None) or (float(creditLine) <= 0):
        print('Credit amount must be greater than 0.')
        json_response['msg'] = 'Credit amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    name, symbol, decimals, totalSupply = \
        eth_api.tokenContractInfo(symbolOrAddr, chain)
    creditLine = float(creditLine) * (10 ** int(decimals))

    try:
        txHash = eth_api.approveERC20(owner, spender, symbolOrAddr, creditLine, chain)
        json_response['body']['resultHash'] = txHash
        json_response['body']['status'] = 'SUCCESS'
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/nft/<chain>/<protocol>', methods=['POST'])
def nftTransaction(chain, protocol):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    sender = args.get('from')
    to = args.get('to')
    data = args.get('data')
    amount = args.get('amount')
    if (sender is None):
        print('From address should not be null.')
        json_response['msg'] = 'From address should not be null.'
        return json.dumps(json_response)
    if (to is None):
        print('To Address should not be null.')
        json_response['msg'] = 'To Address should not be null.'
        return json.dumps(json_response)
    if (data is None):
        print('Data should not be null.')
        json_response['msg'] = 'Data should not be null.'
        return json.dumps(json_response)
    if (amount is None) or (float(amount) < 0):
        print('Mint amount must be greater than 0.')
        json_response['msg'] = 'Mint amount must be greater than 0.'
        return json.dumps(json_response)
    if chain not in ['eth', 'bsc', 'polygon', 'valar']:
        print("Unsupported chain name {}".format(chain))
        json_response['msg'] = "Unsupported chain name {}".format(chain)
        return json.dumps(json_response)

    try:
        txHash = eth_api.nft_tx(sender, to, data, amount, chain)
        json_response['body']['resultHash'] = txHash
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/nft/tokenuri/<chain>/<protocol>', methods=['GET'])
def getNFTMetadata(chain, protocol):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    contract = args.get('contract')
    tokenId = args.get('tokenId')

    # print('INFO: Protocol {} tokenUri on {}, contract {} tokenId {}'.format(
    #     protocol, chain, contract, tokenId
    # ))
    url_eth = "https://eth-mainnet.g.alchemy.com/nft/v2/{}/getNFTMetadata?contractAddress={}&tokenId={}&tokenType={}&refreshCache=false" \
        .format(apikey_alchemy, contract, tokenId, protocol)
    url_goerli = "https://eth-goerli.g.alchemy.com/nft/v2/{}/getNFTMetadata?contractAddress={}&tokenId={}&tokenType={}&refreshCache=false" \
        .format(apikey_alchemy, contract, tokenId, protocol)
    url_polygon = "https://polygon-mainnet.g.alchemy.com/nft/v2/{}/getNFTMetadata?contractAddress={}&tokenId={}&tokenType={}&refreshCache=false" \
        .format(apikey_alchemy, contract, tokenId, protocol)
    url_mumbai = "https://polygon-mumbai.g.alchemy.com/nft/v2/{}/getNFTMetadata?contractAddress={}&tokenId={}&tokenType={}&refreshCache=false" \
        .format(apikey_alchemy, contract, tokenId, protocol)
    url_bsc = "https://deep-index.moralis.io/api/v2/nft/{}/{}?chain=bsc&format=decimal" \
        .format(contract, tokenId)
    url_bsc_test = "https://deep-index.moralis.io/api/v2/nft/{}/{}?chain=0x61&format=decimal" \
        .format(contract, tokenId)

    headers = {"accept": "application/json"}
    if chain not in ['eth', 'bsc', 'polygon', 'goerli', 'mumbai', 'bsc_test']:
        json_response['state'] = 104
        # print("NFT chain cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT chain cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT chain cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if protocol not in ['erc721', 'erc1155']:
        json_response['state'] = 104
        # print("NFT protocol cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT protocol cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT protocol cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if (tokenId is None) or (int(tokenId) <= 0):
        json_response['state'] = 104
        json_response['msg'] = 'tokenId should not be null or negative.'
        print("WARNING: tokenId should not be null or negative.")
        return json.dumps(json_response)
    try:
        if chain == 'eth':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'polygon':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'goerli':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'mumbai':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'bsc':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)
        elif chain == 'bsc_test':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)
        resp = json.loads(r.content.decode())
        # print(resp)
        json_response['body']['status'] = 'SUCCESS'
        if 'metadata' in resp:
            json_response['body']['content'] = resp['metadata']

            return json.dumps(json_response)
        else:
            json_response['body']['content'] = ''
            return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        # print(traceback.format_exc())
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/nft/ownerof/<tokenId>/<chain>/<protocol>', methods=['GET'])
def ownerByToken(tokenId, chain, protocol):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    contract = args.get('contract')

    # print('INFO: Protocol {} tokenUri on {}, contract {} tokenId {}'.format(
    #     protocol, chain, contract, tokenId
    # ))
    url_eth = "https://eth-mainnet.g.alchemy.com/nft/v2/{}/getOwnersForToken?contractAddress={}&tokenId={}" \
        .format(apikey_alchemy, contract, tokenId)

    url_goerli = "https://eth-goerli.g.alchemy.com/nft/v2/{}/getOwnersForToken?contractAddress={}&tokenId={}" \
        .format(apikey_alchemy, contract, tokenId)
    url_polygon = "https://polygon-mainnet.g.alchemy.com/nft/v2/{}/getOwnersForToken?contractAddress={}&tokenId={}" \
        .format(apikey_alchemy, contract, tokenId)
    url_mumbai = "https://polygon-mumbai.g.alchemy.com/nft/v2/{}/getOwnersForToken?contractAddress={}&tokenId={}" \
        .format(apikey_alchemy, contract, tokenId)
    url_bsc = "https://deep-index.moralis.io/api/v2/nft/{}/{}?chain=bsc&format=decimal" \
        .format(contract, tokenId)
    url_bsc_test = "https://deep-index.moralis.io/api/v2/nft/{}/{}?chain=0x61&format=decimal" \
        .format(contract, tokenId)

    headers = {"accept": "application/json"}
    if chain not in ['eth', 'bsc', 'polygon','goerli', 'mumbai', 'bsc_test']:
        json_response['state'] = 104
        # print("NFT chain cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT chain cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT chain cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if protocol not in ['erc721', 'erc1155']:
        json_response['state'] = 104
        # print("NFT protocol cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT protocol cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT protocol cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if (tokenId is None) or (int(tokenId) <= 0):
        json_response['state'] = 104
        json_response['msg'] = 'tokenId should not be null or negative.'
        # print("tokenId should not be null or negative.")
        print("WARNING: tokenId should not be null or negative.")
        return json.dumps(json_response)
    try:
        if chain == 'eth':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'polygon':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'goerli':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'mumbai':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'bsc':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)
        elif chain == 'bsc_test':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)

        resp = json.loads(r.content.decode())
        print(resp)
        json_response['body']['status'] = 'SUCCESS'
        if 'owner_of' in resp:
            json_response['body']['content'] = resp['owner_of']
        elif 'owners' in resp:
            if len(resp['owners']) == 0:
                json_response['body']['content'] = ''
            else:
                json_response['body']['content'] = resp['owners'][0]
        else:
            json_response['body']['content'] = ''
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        # print(traceback.format_exc())
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/nft/totalsupply/<chain>/<protocol>', methods=['GET'])
def totalSupply(chain, protocol):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    contract = args.get('contract')
    # print('INFO: Protocol {} tokenUri on {}, contract {} '.format(
    #     protocol, chain, contract
    # ))
    url_eth = "https://eth-mainnet.g.alchemy.com/nft/v2/{}/getContractMetadata?contractAddress={}" \
        .format(apikey_alchemy, contract)
    url_goerli = "https://eth-goerli.g.alchemy.com/nft/v2/{}/getContractMetadata?contractAddress={}" \
        .format(apikey_alchemy, contract)
    url_polygon = "https://polygon-mainnet.g.alchemy.com/nft/v2/{}/getContractMetadata?contractAddress={}" \
        .format(apikey_alchemy, contract)
    url_mumbai = "https://polygon-mumbai.g.alchemy.com/nft/v2/{}/getContractMetadata?contractAddress={}" \
        .format(apikey_alchemy, contract)
    url_bsc = "https://deep-index.moralis.io/api/v2/nft/{}?chain=bsc&format=decimal" \
        .format(contract)
    url_bsc_test = "https://deep-index.moralis.io/api/v2/nft/{}?chain=0x61&format=decimal" \
        .format(contract)

    headers = {"accept": "application/json"}
    if chain not in ['eth', 'bsc', 'polygon', 'goerli', 'mumbai', 'bsc_test']:
        json_response['state'] = 104
        # print("NFT chain cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT chain cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT chain cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if protocol not in ['erc721', 'erc1155']:
        json_response['state'] = 104
        # print("NFT protocol cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT protocol cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT protocol cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)

    try:
        if chain == 'eth':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'polygon':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'goerli':
            r = requests.get(url_goerli, headers=headers, proxies=proxies)
        elif chain == 'mumbai':
            r = requests.get(url_mumbai, headers=headers, proxies=proxies)
        elif chain == 'bsc':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)
        elif chain == 'bsc_test':
            headers = {
                "accept": "application/json",
                "X-API-Key": apikey_moralis
            }
            r = requests.get(url_bsc_test, headers=headers, proxies=proxies)

        resp = json.loads(r.content.decode())
        print(resp)
        json_response['body']['status'] = 'SUCCESS'
        if 'contractMetadata' in resp:
            json_response['body']['content'] = resp['contractMetadata']['totalSupply']
        elif chain == 'bsc':
            json_response['body']['content'] = resp['total']
        else:
            json_response['body']['content'] = ''
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        # print(traceback.format_exc())
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


# 根据NFT合约批量获取tokenId、tokenUri、ownerAddress等
@app.route('/nft/tokenall/<chain>/<protocol>', methods=['GET'])
def tokenAll(chain, protocol):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    contract = args.get('contract')
    param = args.get('param')

    # print('INFO: NFT contract {} ownership on {}.'.format(
    #     contract, chain))

    if chain not in ['eth', 'bsc', 'polygon', 'goerli', 'mumbai', 'bsc_test']:
        json_response['state'] = 104
        # print("NFT chain cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT chain cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT chain cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)

    if chain == 'bsc':
        chain = '0x61'
    elif chain == 'eth':
        chain = 'goerli'
    elif chain == 'polygon':
        chain = 'mumbai'
    url_ = "https://deep-index.moralis.io/api/v2/nft/{}/owners?chain={}" \
        .format(contract, chain)
    try:
        headers = {
            "accept": "application/json",
            "X-API-Key": apikey_moralis
        }
        r = requests.get(url_, headers=headers, proxies=proxies)
        resp = json.loads(r.content.decode())
        # print(resp)
        json_response['body']['status'] = 'SUCCESS'
        try:
            json_response['body']['content'] = resp['result']
        except:
            json_response['body']['content'] = ''
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


# 扫描某个地址的NFT资产记录
@app.route('/nft/assets/<chain>/<wallet>', methods=['GET'])
def nftAssets(chain, wallet):
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    # print('INFO: Querying wallet {} NFT assets ownership on {}.'.format(
    #     wallet, chain
    # ))

    if chain not in ['eth', 'bsc', 'polygon', 'goerli', 'bsc_test', 'mumbai']:
        json_response['state'] = 104
        # print("NFT chain cannot be empty or {} is not supported".format(chain))
        print("WARNING: NFT chain cannot be empty or {} is not supported".format(chain))
        json_response['msg'] = "NFT chain cannot be empty or {} is not supported".format(chain)
        return json.dumps(json_response)
    if chain == 'bsc':
        chain = '0x61'
    elif chain == 'eth':
        chain = 'goerli'
    elif chain == 'polygon':
        chain = 'mumbai'
    url_ = "https://deep-index.moralis.io/api/v2/{}/nft?chain={}&format=decimal" \
        .format(wallet, chain)
    try:
        headers = {
            "accept": "application/json",
            "X-API-Key": apikey_moralis
        }
        r = requests.get(url_, headers=headers, proxies=proxies)
        resp = json.loads(r.content.decode())
        json_response['body']['status'] = 'SUCCESS'
        result = resp['result']
        try:
            content_list = []
            for n in result:
                new_n = {}
                for k,v in n.items():
                    if k in ('amount', 'token_address', 'token_id'):
                        new_n[k] = v
                content_list.append(new_n)
            json_response['body']['content'] = content_list
        except:
            print(traceback.format_exc())
            json_response['body']['content'] = ''
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


# 用地址的私钥对十六进制信息进行加密签名，返回字符串。
@app.route('/sign-message', methods=['POST'])
def sign_message():
    json_response = copy.deepcopy(response_template)
    json_response['body']['time'] = int(time.time())
    args = request.args
    sender = args.get('_from')
    message = args.get('message')

    try:
        sig = eth_api.sign_msg(sender, message)
        json_response['body']['signature'] = sig
        return json.dumps(json_response)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.format_exc())
        json_response['state'] = 199
        json_response['msg'] = str(ex_value)
        return json.dumps(json_response)


@app.route('/getfile', methods=['POST'])
def getfile():
    file = request.files['file']
    txt = file.read().decode()
    with open('./wallet/keystore_migrate.txt', 'w') as f:
        f.write(txt)
    f.close()
    return 'success'

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5001)
