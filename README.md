
##  Authentication must be added for external requests

1. Install necessary packages from requirements.txt
2. If running as a standalone service, execute command: python main.py 


### Generate TRC20/ERC20 address: **/creation/address/{type}** `POST`

###### Parameters:
* `{type}` _ Range: trc20 | erc20 _ 'Mandatory'
###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "address": "TDX5JMyM15sDxHSJa61kt7s8Kx3tmYSRVd",
        "status": "NEW",
        "time": 1644569157421
    }
}
```


### Get address info: **/account/{type}** `GET`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `address` _account address_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "id": "",
        "name": "Test001", // account name
        "balance": "1886.45932", // account balance
        "address": "xxxxxxxxxx",// TRC20 | ERC20
        "createTime": 1624002276000 
    }
}
```


### Get info on Contract Address or token: **/contract/{type}/{symbolOrAddr}** `GET`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `{symbolOrAddr}` _token symbol or Contract Address 'Mandatory'
* `from` _address_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "name": "Test Token 01", // token name
        "symbol": "TET", // token symbol
        "decimals": 6,// token decimals
        "totalSupply": 100000000 // total supply
    }
}
```


### Get ERC20/TRC20 balance of address: **/balance/{type}** `GET`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `address` _address_ 'Mandatory'
* `symbolOrAddr` _symbol or Contract Address 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "balance": "1023.325",
        "symbolOrAddr": "usdt",
        "address": "TVvd6UhfRnQoAUUQqpStXpyWasbFWKmLNb" // erc20 | trc20
    }
}
```


### Get token decimals: **/decimals/{type}/{symbolOrAddr}** `GET`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `{symbolOrAddr}` _token symbol or Contract Address 'Mandatory'
* `owner` _address_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "decimals": 18,
        "symbolOrAddr": "usdt" // token symbol or Contract Address, depending on url parameters
    }
}
```


### send TRX/ETH to address: **/transfer/{symbol}** `POST`

###### parameters:
* `{symbol}` _ Range: trx | eth_ 'Mandatory'
* `from` _sender_ 'Mandatory'
* `to` _receiver_ 'Mandatory'
* `amount` _amount_ 'Mandatory'
* `chain` _Range: eth(Default) | bsc | polygon | _  'Optional'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "8008ea0645787161c76205e2e6e4989d4e6d6542d5a9f350807904b9864a2ad0",
        "time": 1644748690254
    }
}


### Send TRC20/ERC20 token to address: **/transfer/{type}** `POST`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `from` _sender_ 'Mandatory'
* `to` _receiver_ 'Mandatory'
* `amount` _amount_ 'Mandatory'
* `symbolOrAddr` _token symbol or Contract Address_ 'Mandatory'
* `memo` _memo that goes on chain_  'Optional'
* `chain` _Range: eth(Default) | bsc | polygon | _  'Optional'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```


### send on behalf TRC20/ERC20 to address: **/transferFrom/{type}** `POST`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `from` _sender_ 'Mandatory'
* `to` _receiver_ 'Mandatory'
* `spender` _spender that sends the tx_ 'Mandatory'
* `amount` _amount_ 'Mandatory'
* `symbolOrAddr` _token symbol or Contract Address_ 'Mandatory'
* `memo` _memo that goes on chain_  'Optional'
* `chain` _Range: eth(Default) | bsc | polygon | _  'Optional'


###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "xxxxxxxxxxxxxxxx",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```




### Mint token: **/mint/{chain}/erc20/{symbolOrAddr}** `POST`

###### parameters:
* `{chain}` _Range: eth(Default) | bsc | polygon | _ 'Mandatory'
* `{symbolOrAddr}` _token symbol or Contract Address_ 'Mandatory'
* `owner` _Contract owner_ 'Mandatory'
* `amount` _amount_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```

### Burn tokens: **/burn/{chain}/erc20/{symbolOrAddr}** `POST`

###### parameters:
* `{chain}` _Range: eth(Default) | bsc | polygon | _ 'Mandatory'
* `{symbolOrAddr}` _token symbol or Contract Address_ 'Mandatory'
* `owner` _Contract owner_ 'Mandatory'
* `amount` _amount_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```


### Send tx authorisation: **/approve/{type}** `POST`

###### parameters:
* `{type}` _ Range: trc20 | erc20_ 'Mandatory'
* `owner` _authorisor_ 'Mandatory'
* `spender` _spender that actually sends a transaction_ 'Mandatory'
* `symbolOrAddr` _token symbol or Contract Address_ 'Mandatory'
* `creditLine` _credit sent from owner to spender, Default`10000000`_  'Optional'
* `memo` _memo that goes on chain_  'Optional'
* `chain` _Range: eth(Default) | bsc | polygon | _  'Optional'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```

### Deploy ERC20 token Contract: **/deploy/{chain}/erc20** `POST`

###### parameters:
* `{chain}` _ Range: eth | bsc | polygon 'Mandatory'
* `owner` _Contract creator_ 'Mandatory'
* `name` _token name_ 'Mandatory'
* `symbol` _token symbol_ 'Mandatory'
* `decimals` _token decimals,  Range: 1-20_  'Optional'
* `totalSupply` _Token total supply, eg: 100000_  'Optional'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "xxxxxxxxxxxxxxxxxxxx",
        "content": "xxxxxxxxxxxxxxx",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```

### NFT transaction: **/nft/{chain}/{protocol}** `POST`

###### parameters:
* `{chain}` _Network: eth | bsc | polygon | _ 'Mandatory'
* `{protocol}` _NFT protocol Range: erc721 | erc1155_ 'Mandatory'
* `from` _tx sender_ 'Mandatory'
* `to` _Contract Address_ 'Mandatory'
* `data` _ value after Function.encode_ 'Mandatory'
* `amount` _tx amount Default`0.00`_  'Optional'

###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "xxxxxxxxxxxxxxxxxxxxxx",
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```


### Query NFT metadata: **/nft/tokenuri/{chain}/{protocol}** `GET`

###### parameters:
* `{chain}` _Network: eth | bsc | polygon | _ 'Mandatory'
* `{protocol}` _NFT protocol Range: erc721 | erc1155_ 'Mandatory'
* `contract` _Contract Address_ 'Mandatory'
* `tokenId` _NFT的Token Id_ 'Mandatory'
* `funcName` _ Range: tokenURI(Default) | uri_  'Optional'


###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "https://xxx.ipfs.io/xx/c.json", // token uri, ""for not found
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```

### Get owner of NFT by TokenID: **/nft/ownerof/{tokenId}/{chain}/{protocol}** `GET`

###### parameters:
* `{tokenId}` _&ge;0 string_ 'Mandatory'
* `{chain}` _Network: eth | bsc | polygon | _ 'Mandatory'
* `{protocol}` _NFT protocol Range: erc721 | erc1155_ 'Mandatory'
* `contract` _Contract Address_ 'Mandatory'


###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "0xxxxxxxxxxxxx",// "" for not found
        "status": "SUCCESS", // FAILED 
        "time": 1644749120341
    }
}
```

### Get total supply of nft **/nft/totalsupply/{chain}/{protocol}** `GET`

###### parameters:
* `{chain}` _Network: eth | bsc | polygon | _ 'Mandatory'
* `{protocol}` _NFT protocol Range: erc721 | erc1155_ 'Mandatory'
* `contract` _Contract Address_ 'Mandatory'


###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "3056",// totalSupply, "" for not found
        "status": "SUCCESS", // FAILED for failure to send tx 
        "time": 1644749120341
    }
}
```



### Batch query tokenId, tokenUri, ownerAddress, etc. for nft contract: **/nft/tokenall/{chain}/{protocol}** `GET`

###### parameters:
* `{chain}` _Network: eth | bsc | polygon | _ 'Mandatory'
* `{protocol}` _NFT protocol，range: erc721 | erc1155_ 'Mandatory'
* `contract` _Contract Address_ 'Mandatory'


###### return:
```
{
    "state": 200,
    "msg": "Successful",
    "body":{
        "totalSupply": 0 // 0 for not found
    }
}
```

```
[{
    "chainName": "ETH",
    "protocl": "erc721",
    "contract":"0x0574c34385b039c2bb8db898f61b7767024a9449", // NFTContract Address
    "index":940,   // Contract index
    "tokenId":"941", // token Id
    "owner":"0x46e0dcceb5357f1c59a9de1b29173f85ddb8198f", // owner address
    "url":"https://joyworld.azurewebsites.net/api/HttpTrigger?id\u003d941", // token URI
    "time":1649836589785
}]
```



### NFT assets under address: **/nft/assets/{chain}/{address}** `GET`

###### parameters:
* `{chain}` _Network: eth | bsc | polygon_ 'Mandatory'
* `{address}` _Wallet Address_ 'Mandatory'

###### return:
```
{
    "state": 200,
    "msg": "Successful"
}
```

```
[
  {
    "chainName":"ETH",
    "protocol": "ERC721",
    "address":  "Wallet Address",
    "amount":    "NFT amount under address",
    "name":     "NFT name",
    "contract": "NFT Contract", 
    "symbol":   "NFT symbol",
    "tokenIds": ["tokenID", "tokenID"]
  }
]
```
