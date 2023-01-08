# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/10 10:17
# @Author : masai
# @Email :
# @File : api.py
# @Software: PyCharm
import web3
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract, Contract
from web3.middleware import geth_poa_middleware
import json
from utils.decorator import *
import binascii
from eth_account.messages import encode_defunct
import time
from random import choice
from solcx import compile_standard, install_solc
install_solc('0.6.0')
from config import rpc
from eth_account import Account
env = 'test'
# env = 'mainnet'
if env == 'test':
    w3_eth_list =[Web3(Web3.HTTPProvider(rpc.goerli_rpc[k], request_kwargs=\
        {"proxies": {'https': None, 'http': None}})) for k,v in rpc.goerli_rpc.items()]

    w3_bsc_list = [Web3(Web3.HTTPProvider(rpc.bsc_test_rpc[k], request_kwargs=\
        {"proxies": {'https': None, 'http': None}})) for k,v in rpc.bsc_test_rpc.items()]

    w3_polygon_list = [Web3(Web3.HTTPProvider(rpc.polygon_test_rpc[k], request_kwargs=\
        {"proxies": {'https': None, 'http': None}})) for k,v in rpc.polygon_test_rpc.items()]

    w3_valar_list = [Web3(Web3.HTTPProvider(rpc.valar_test_rpc[k], request_kwargs=\
        {"proxies": {'https': None, 'http': None}})) for k,v in rpc.valar_test_rpc.items()]
    chainid_eth = 5
    chainid_bsc = 97
    chainid_polygon = 80001
    chainid_valar = 1203

elif env == 'mainnet':
    w3_eth_list = [Web3(Web3.HTTPProvider(rpc.eth_rpc[k], request_kwargs= \
        {"proxies": {'https': None, 'http': None}})) for k, v in rpc.eth_rpc.items()]

    w3_bsc_list = [Web3(Web3.HTTPProvider(rpc.bsc_rpc[k], request_kwargs= \
        {"proxies": {'https': None, 'http': None}})) for k, v in rpc.bsc_rpc.items()]

    w3_polygon_list = [Web3(Web3.HTTPProvider(rpc.polygon_rpc[k], request_kwargs= \
        {"proxies": {'https': None, 'http': None}})) for k, v in rpc.polygon_rpc.items()]

    chainid_eth = 1
    chainid_bsc = 56
    chainid_polygon = 137
    chainid_valar = 1203
# print(w3_default.isConnected())
migrated_addresses = set()
with open('./wallet/migrated_addresses.txt', 'r') as f:
    addr = f.readlines()
    for a in addr:
        migrated_addresses.add( '0x'+ a.replace('\n', ''))

print('Loaded this many migrated addresses into memory: ',len(migrated_addresses))

w3=''
def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')


def hexStr_to_str(hex_str):
    hexi = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hexi)
    return str_bin.decode('utf-8')

#
# def getLogs(address, chain='goerli'):
#     addr = w3.toChecksumAddress(address)
#     logs = w3.eth.get_logs({'fromBlock': 765178, 'toBlock': 765178})
#
#     # logs = w3.eth.get_logs({'address':addr})
#     print(logs)
#     return logs

@retry_decorator
def getBalance(wallet, chain='eth'):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
    elif chain == 'valar':
        w3 = choice(w3_valar_list)

    wallet = w3.toChecksumAddress(wallet)
    balance = w3.eth.getBalance(wallet)
    # print(balance)
    return balance


@retry_decorator
def getBalanceByToken(address, contract, chain):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    address = w3.toChecksumAddress(address)
    contract = w3.toChecksumAddress(contract)
    contract = getContract(contract, chain)
    balance = contract.functions.balanceOf(address).call()
    return balance


@retry_decorator
def sendTransaction(send_from, value, send_to, gas=1000000, chain='eth'):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
        chain_Id = chainid_valar

    from_address = send_from
    to_address = send_to
    # Implement internal private key fetching for from_address here
    private_key = getPK(from_address)
    nonce = w3.eth.getTransactionCount(from_address)
    print('nonce: ',nonce)
    value = w3.toWei(value, 'ether')

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': gas,
        'gasPrice': int(w3.eth.gasPrice*1.01),
        # 'data': data,
        "chainId": chain_Id
    }
    # sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Print transaction hash in hex
    print(w3.toHex(tx_hash))
    return w3.toHex(tx_hash)


def getBlockNumber(chain='goerli'):
    blockNumber = w3.eth.blockNumber
    # print(blockNumber)
    return blockNumber


def getTransaction(transaction_hash=None, chain='goerli'):
    tx_json = w3.eth.getTransaction(transaction_hash)
    print(tx_json)
    return tx_json


@retry_decorator
def getContract(address, chain='eth'):
    abi = """[{"type":"constructor","stateMutability":"nonpayable","payable":false,"inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"spender","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Swap","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount0Out","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1Out","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Sync","inputs":[{"type":"uint112","name":"reserve0","internalType":"uint112","indexed":false},{"type":"uint112","name":"reserve1","internalType":"uint112","indexed":false}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DOMAIN_SEPARATOR","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"MINIMUM_LIQUIDITY","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"PERMIT_TYPEHASH","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"amount0","internalType":"uint256"},{"type":"uint256","name":"amount1","internalType":"uint256"}],"name":"burn","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"initialize","inputs":[{"type":"address","name":"_token0","internalType":"address"},{"type":"address","name":"_token1","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"kLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"mint","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"nonces","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"permit","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price0CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price1CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"skim","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"swap","inputs":[{"type":"uint256","name":"amount0Out","internalType":"uint256"},{"type":"uint256","name":"amount1Out","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"sync","inputs":[],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false}]"""
    if chain == 'eth':
        w3 = choice(w3_eth_list)
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
    # address = w3.toChecksumAddress(address)
    contract = w3.eth.contract(address=address, abi=abi, ContractFactoryClass=Contract)
    # functions = contract.all_functions()
    # print(functions)
    return contract


def tokenContractInfo(address, chain):
    contract = getContract(address, chain)
    totalSupply = contract.functions.totalSupply().call()
    decimals = contract.functions.decimals().call()
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    return name, symbol, decimals, totalSupply


def addWallet(privateKeySender):
    web3.eth.accounts.wallet.add(privateKeySender)
    # w3.eth.accounts
    return

@retry_decorator
def createAccount(chain='eth'):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
    new_account = w3.eth.account.create()
    addr = str(new_account._address)
    # print('Created: ', new_account._address, (new_account._private_key).hex())
    with open('./wallet/' + addr.lower() + '.keystore', 'w') as f:
        f.write(json.dumps(new_account.encrypt('password')))
    f.close()
    return addr


def getPK(addr):
    with open('./wallet/' + str(addr).lower() + '.keystore', 'r') as f:
        encrypted = f.read()
    f.close()
    if str(addr).lower() in migrated_addresses:
        pk = Account.decrypt(encrypted, '')
    else:
        pk = Account.decrypt(encrypted, 'password')
    # print(pk.hex())
    return pk.hex()


def process_keystore_migrate():
    with open('./wallet/keystore.txt','r') as f:
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


@retry_decorator
def deployERC20(owner, name, symbol, totalSupply, decimals, chain):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
        chain_Id = chainid_valar

    with open('./contracts/tokenERC20.sol', 'r') as file:
        erc20 = file.read()
    file.close()
    compiled_erc20 = compile_standard(
        {
            "language": "Solidity",
            "sources": {"tokenERC20.sol": {"content": erc20}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.6.0",
    )
    # with open('./contracts/compiled_erc20.json', 'w') as file:
    #     json.dump(compiled_erc20, file)
    # file.close()
    bytecode = compiled_erc20["contracts"]["tokenERC20.sol"]["TokenERC20"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_erc20["contracts"]["tokenERC20.sol"]["TokenERC20"]["metadata"])["output"]["abi"]
    erc20_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get
    TransactionCount(owner)
    tx = erc20_contract.constructor(totalSupply, decimals, name, symbol).build_transaction(
        {'chainId': chain_Id, 'from': owner, 'nonce': nonce, 'gas': 3000000,
         'gasPrice': int(w3.eth.gasPrice * 1.01)}
    )
    # implement pk here
    private_key = getPK(owner)
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('Deploy erc20 tx hash: ', Web3.toHex(tx_hash))
    print('Deploy erc20 address: ', tx_receipt['contractAddress'])
    return Web3.toHex(tx_hash), tx_receipt['contractAddress']

@retry_decorator
def callERC20(operation, sender, receiver, amount, contractERC20, chain, spender=None):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
        chain_Id = chainid_valar
    if receiver != '':
        receiver = w3.toChecksumAddress(receiver)
    contractERC20 = w3.toChecksumAddress(contractERC20)
    with open('./contracts/tokenERC20.sol', 'r') as file:
        erc20 = file.read()
    file.close()
    compiled_erc20 = compile_standard(
        {
            "language": "Solidity",
            "sources": {"tokenERC20.sol": {"content": erc20}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.6.0",
    )
    abi = json.loads(compiled_erc20["contracts"]["tokenERC20.sol"]["TokenERC20"]["metadata"])["output"]["abi"]

    contract = w3.eth.contract(address=contractERC20, abi=abi)
    nonce = w3.eth.get_transaction_count(sender)
    # implement pk fetching
    private_key = getPK(sender)
    if spender:
        private_key = getPK(spender)

    if operation == 'transfer':
        token_tx = contract.functions.transfer(receiver, int(amount)).\
            build_transaction({'chainId':chain_Id, 'gas':1000000, 'nonce':nonce,
                               'gasPrice': int(w3.eth.gasPrice * 1.01)})

    elif operation == 'transferFrom':
        token_tx = contract.functions.transferFrom(sender, receiver, int(amount)).\
            build_transaction({'chainId':chain_Id, 'gas':1000000, 'nonce':nonce,
                               'gasPrice': int(w3.eth.gasPrice * 1.01)})

    elif operation == 'mint':
        token_tx = contract.functions.mint(int(amount)).\
            build_transaction({'chainId': chain_Id, 'gas': 1000000, 'nonce': nonce,
                               'gasPrice': int(w3.eth.gasPrice * 1.01)})
    elif operation == 'burn':
        token_tx = contract.functions.burn(int(amount)).\
            build_transaction({'chainId': chain_Id, 'gas': 1000000, 'nonce': nonce,
                               'gasPrice': int(w3.eth.gasPrice * 1.01)})

    signed_token_tx = w3.eth.account.sign_transaction(token_tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_token_tx.rawTransaction)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(Web3.toHex(tx_hash))
    return Web3.toHex(tx_hash)

@retry_decorator
def approveERC20(owner, spender, contractERC20, creditLine, chain):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
        chain_Id = chainid_valar

    owner = w3.toChecksumAddress(owner)
    spender = w3.toChecksumAddress(spender)
    contractERC20 = w3.toChecksumAddress(contractERC20)
    with open('./contracts/tokenERC20.sol', 'r') as file:
        erc20 = file.read()
    file.close()
    compiled_erc20 = compile_standard(
        {
            "language": "Solidity",
            "sources": {"tokenERC20.sol": {"content": erc20}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.6.0",
    )
    abi = json.loads(compiled_erc20["contracts"]["tokenERC20.sol"]["TokenERC20"]["metadata"])["output"]["abi"]

    contract = w3.eth.contract(address=contractERC20, abi=abi)
    nonce = w3.eth.get_transaction_count(owner)
    # implement pk fetching
    private_key = getPK(owner)
    token_tx = contract.functions.approve(spender, int(creditLine)).\
        build_transaction({'chainId': chain_Id, 'gas':1000000, 'nonce':nonce,
                           'gasPrice': int(w3.eth.gasPrice * 1.01)})
    signed_token_tx = w3.eth.account.sign_transaction(token_tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_token_tx.rawTransaction)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('Approve erc20 hash:',  Web3.toHex(tx_hash))
    return Web3.toHex(tx_hash)

@retry_decorator
def nft_tx(sender, to_contract, data, amount, chain):
    if chain == 'eth':
        w3 = choice(w3_eth_list)
        chain_Id = chainid_eth
    elif chain == 'bsc':
        w3 = choice(w3_bsc_list)
        chain_Id = chainid_bsc
    elif chain == 'polygon':
        w3 = choice(w3_polygon_list)
        chain_Id = chainid_polygon
    elif chain == 'valar':
        w3 = choice(w3_valar_list)
        chain_Id = chainid_valar

    sender = w3.toChecksumAddress(sender)
    to_contract = w3.toChecksumAddress(to_contract)
    nonce = w3.eth.get_transaction_count(sender)
    # implement pk fetching
    private_key = getPK(sender)
    token_tx = {'to': to_contract, 'data': data,  'gas': 3000000, 'chainId':chain_Id,
                'gasPrice': int(w3.eth.gasPrice * 1.01), 'nonce': nonce}
    signed_token_tx = w3.eth.account.sign_transaction(token_tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_token_tx.rawTransaction)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('nft_tx hash:', Web3.toHex(tx_hash))
    return Web3.toHex(tx_hash)

# sign a hex message with private key of sender. returns string.
def sign_msg(sender, msg):
    w3 = choice(w3_eth_list)
    sender = w3.toChecksumAddress(sender)
    private_key = getPK(sender)
    b = bytes.fromhex(msg)
    msghash = encode_defunct(text=b.decode())
    sig = w3.eth.account.sign_message(msghash, private_key)
    return sig[-1].hex()

if __name__ == '__main__':
    usdt_goerli = '0x509Ee0d083DdF8AC028f2a56731412edD63223B9'
    myAccount1 = '0xE931040A5112f0F822c513eB025ACA65F094654B'
    myAccount2 = '0xD046336230ee654cB9CaA4AcA690EAe0e37CF8ab'
    myAccount3 = '0x899Ba0df19Bf8AF9de0A6Ccc5fE63512C7477bb2'
    myAccount4 = '0xe25838D7d04F32aA40028a76B2f23C6CD47cC8b9'
    myAccount5 = '0x40a1Ff27c27360BA4C65bc8c0962ED81D3a1bB4a'

    pk2 = '9b1b95c72aed704124fdeb5fb823291f358f9a9b956114c7e2064aa1c53c8d46'
    pk3 = 'e4c46fca983502aa39adae992600b82541dcfc393dd2a12e1aa3ea43f2f64aee'
    erc20_xgs = '0xc7063da9532e15c8eeea06befbd2c50f29c83d4d'

    # a = getPK('0x40a1Ff27c27360BA4C65bc8c0962ED81D3a1bB4a')
    # print(a)
    # # deployERC20(myAccount3, pk3, 'T2', 'T2', 2222, 11, 'p')
    # # sendTransaction(myAccount3, 0.02, myAccount2)
    # # sendERC20(myAccount3, myAccount2, 333, erc20_xgs)
    # a = sign_msg('0xa628920964099929f6f254b3e04f0bb337f5ef87', '36343835303961312d363361652d343363352d393165392d623630613661623433643663')
    # print(a)
    # t = """{"address":"515410e183dda62f13ee407f7f86c131426b5b74","id":"ae0d47f5-ad5a-42ff-aae8-2d1775bfb2ab","version":3,"crypto":{"cipher":"aes-128-ctr","ciphertext":"26b6b2c30940a7c52583e66a181ad63b853995ba78b5da6ed77da0a629654eb7","cipherparams":{"iv":"23be38b36aff4aadc1b1847791c2c348"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":4096,"p":6,"r":8,"salt":"044cc08022ca8c75b5a66258c144c043befd75a8c8db7ec22af2dee55cdb4ae9"},"mac":"6b988320736c6cd38ab865e4692c39cd60da57b3c2814420d26a110f7e1d1fbb"}}"""
    # pk = Account.decrypt(t, '')
    # print('111', pk.hex())
    process_keystore_migrate()
    # a = sign_msg('0xe25838d7d04f32aa40028a76b2f23c6cd47cc8b9', '36343835303961312d363361652d343363352d393165392d623630613661623433643663')
    # print(a)