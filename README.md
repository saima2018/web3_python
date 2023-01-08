# web3_python
A python service with common necessary methods to interact with EVM blockchains 

关于API请求说明:

API服务为授权请求，除了白名单的URL请求外，所有请求都需经过Token认证。
非白名单请求，需要传递相应的参数，传递参数规范如下：




参数名
传递要求
说明




appId
Header
当前的APPID


time
Header
当前请求时间戳(ms)，每次请求时获取最新的时间戳 单次请求有效时长30s



token
Header
请求的Token Token是基于HMAC-SHA256加密验证





token生成策略

1.对http request中(GET/POST)的参数组装为键值对：key=value
2.对键值对进行ASCII升序排列
3.排列后的键值对使用 '&' 进行拼接: key1=value1&key2=value2
4.对第三步的字符串使用secretKey进行HMAC-SHA256签名，从而得到token



示例伪代码：
如(GET/POST)请求参数：name=Smith, id=2922
header参数: appId=20070948372, time=1502342342235

String[] params = [GET/POST请求参数, header参数]
Arrays.sort(params);// ASCII升序排序(稳定排序)

StringBuilder strBuilder = new StringBuilder();
params.foreach(str -> strBuilder.append(str).append("&"));// 拼接所有参数
String resultStr = strBuilder.substring(0, strBuilder.length() - 1);

// 得到token
String token = hmac_sha256(resultStr, secretKey);// HMAC-SHA256

// 添加进请求的header参数 
appId=20070948372, time=1502342342235, token=上方生成的token



API返回状态说明:

199        Failure (失败)
200        Successful (成功)

101        API not found (未知的API请求)
102        Token verification failed (Token验证失败)
103        Token has expired (Token已过期)
104        Parameter error (请求的参数错误)
110        Service internal error (服务内部错误)



生成TRC20/ERC20地址: /creation/address/{type} POST


参数:


{type} 取值范围: trc20 | erc20 (BEP20也使用erc20) 必选


ownerAddress 仅type为trc20时，可使用ownerAddress激活新生成地址, 须确保ownerAddress账户>2 TRX 可选


accountName 仅type为trc20时，可修改新地址的账户名称, 需确保区块链网络唯一。如有该参数, 需同时传入ownerAddress地址 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "address": "TDX5JMyM15sDxHSJa61kt7s8Kx3tmYSRVd",
        "status": "NEW", // 见下方返回字段说明
        "time": 1644569157421
    }
}



返回参数status字段说明:



状态
顺序
说明




ALL
5
全部完成


APPROVED
4
授信完成


TRANSFER
3
转入TRX完成


ACTIVATED
2
激活完成(当授信额>0时, 此步跳过)


NEW
1
已生成新地址




生成TRC20新地址(含自动激活、授信): /autocreation/address/trc20 POST


参数:


spender 授信受托人地址, 该地址账户的TRX≥10, 否则可能激活与授信失败 必选


symbolOrAddr 代币符号或合约地址, 如: USDT、TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t 必选


accountName 账户名称，为地址指定账户名称, 需确保区块链网络唯一 可选


transferTrx 从spender向新生成地址转入TRX数量, 便于激活和授信使用, 默认10 可选


creditLine 授信额度, 新地址向spender地址授信, 默认10000000 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "address": "TDX5JMyM15sDxHSJa61kt7s8Kx3tmYSRVd",
        "status": "ALL", // 见上方说明
        "time": 1644569157421
    }
}



获取一个地址账户信息: /account/{type} GET


参数:


{type} 取值范围: trc20 | erc20 必选


address 账户地址 必选


chain 当type=erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "id": "",
        "name": "Test001", // 账户名称
        "balance": "1886.45932", // 账户总价值（单位: TRX|ETH）
        "address": "TVvd6UhfRnQoAUUQqpStXpyWasbFWKmLNb",// TRC20 | ERC20
        "createTime": 1624002276000 // 0:表示未知
    }
}



获取一个合约地址或代币信息: /contract/{type}/{symbolOrAddr} GET


参数:


{type} 取值范围: trc20 | erc20 必选


{symbolOrAddr} 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


from 账户地址 必选


chain 当type=erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "name": "Test Token 01", // token 名称
        "symbol": "TET", // token符号
        "decimals": 6,// token精度
        "totalSupply": 100000000 // 总发行量:1亿
    }
}



获取一个地址的ERC20/TRC20代币余额: /balance/{type} GET


参数:


{type} 取值范围: trc20 | erc20 必选


address 账户地址 必选


symbolOrAddr 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


chain 当type=erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "balance": "1023.325",
        "symbolOrAddr": "usdt",
        "address": "TVvd6UhfRnQoAUUQqpStXpyWasbFWKmLNb" // erc20 | trc20
    }
}



获取一个代币精度: /decimals/{type}/{symbolOrAddr} GET


参数:


{type} 取值范围: trc20 | erc20 必选


{symbolOrAddr} 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


owner 账户地址 必选


chain 当type=erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "decimals": 18,
        "symbolOrAddr": "usdt" // 代币符号或合约地址，取决于URL的参数
    }
}



向一个地址转出TRX/ETH: /transfer/{symbol} POST


参数:


{symbol} 取值范围: trx | eth 必选


from 付款地址 必选


to 收款地址 必选


amount 转账数量 必选


param 回调参数, 需URL Encode编码。当交易被确认固化后, 触发回调。 可选


chain 当{symbol}为eth时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "8008ea0645787161c76205e2e6e4989d4e6d6542d5a9f350807904b9864a2ad0",
        "time": 1644748690254
    }
}



TRX转账回调Json格式:

{
    "resultHash":"2d0cab65f2530a9a5192c0b9daa0a6380b981507cb49fa44153b57a92adbeec0",
    "status": "SUCCESS", // FAILED 表示发送交易失败
    "time":1644750266224
}



向一个地址转出TRC20/ERC20的代币: /transfer/{type} POST


参数:


{type} 取值范围: trc20 | erc20 必选


from 付款地址 必选


to 收款地址 必选


amount 转账数量 必选


symbolOrAddr 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


memo 备注内容, 同步到区块链交易中 可选


param 回调参数, 需URL Encode编码。当交易被确认固化后, 触发回调。 可选


chain 当{type}为erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



向一个地址委托转出TRC20/ERC20的代币: /transferFrom/{type} POST


参数:


{type} 取值范围: trc20 | erc20 必选


from 付款地址 必选


to 收款地址 必选


spender 受托人地址, spender地址操作from地址转账给to地址 必选


amount 转账数量 必选


symbolOrAddr 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


memo 备注内容, 同步到区块链交易中 可选


param 回调参数, 需URL Encode进行编码。当交易被确认固化后, 触发回调。 可选


chain 当{type}为erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



trc20 transfer/transferFrom 回调Json格式:

{
    "resultHash":"5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
    "status": "SUCCESS", // FAILED 表示发送交易失败
    "confirmed": "REVERT", // SUCCESS 表示区块链确认成功
    "time":1644749120341
}



增发代币: /mint/{chain}/erc20/{symbolOrAddr} POST


参数:


{chain} 当{type}为erc20时，取值范围：eth(默认) | bsc | polygon | valar 必选


{symbolOrAddr} 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


owner 合约拥有人地址 必选


amount 增发数量，需大于0。如增发10万, 表示:100000 必选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



销毁代币: /burn/{chain}/erc20/{symbolOrAddr} POST


参数:


{chain} 当{type}为erc20时，取值范围：eth(默认) | bsc | polygon | valar 必选


{symbolOrAddr} 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


owner 合约拥有人地址 必选


amount 销毁数量，需大于0。如销毁10万, 表示:100000 必选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



发起授信委托: /approve/{type} POST


参数:


{type} 取值范围: trc20 | erc20 必选


owner 委托发起人/实际转出地址, 该地址账户的TRX≥10或ETH≥0.0055(价值≥15usdt), 否则可能授信失败 必选


spender 委托受托人/发起转账操作的地址 必选


symbolOrAddr 代币符号或合约地址, 如USDT、0x4008D09B0BD2B96E3325D43da778D545E9fa9104 必选


creditLine 授信额度, owner地址向spender地址授信转账额度, 默认10000000 可选


memo 备注内容, 同步到区块链交易中 可选


param 回调参数, 需URL Encode编码。当交易被确认固化后, 触发回调。 可选


chain 当{type}为erc20时，取值范围：eth(默认) | bsc | polygon | valar 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



部署ERC20代币合约: /deploy/{chain}/erc20 POST


参数:


{chain} 取值范围: eth | bsc | polygon | valar 必选


owner 合约创建人地址 必选


name 代币名称 必选


symbol 代币符号 必选


decimals 代币精度, 取值范围: 1-20 可选


totalSupply 代币发行总量, 如10万总量: 100000 可选


param 回调参数, 需URL Encode编码。当交易被确认固化后, 触发回调。 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "content": "0x84ecf4c860f6b5a02ed5e879910d85515f2efa19",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



NFT交易: /nft/{chain}/{protocol} POST


参数:


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


from 发起交易的地址 必选


to 合约地址 必选


data 经Function.encode的值 必选


amount 交易数量,需自乘精度。默认0.00 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "resultHash": "5b6fda8cf8755ffd7e1ab20502369ad32a3726471e0bf63de7d68106284b23f6",
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



查询NFT元数据: /nft/tokenuri/{chain}/{protocol} GET


参数:


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


contract 合约地址 必选


tokenId NFT的Token Id 必选


funcName 取值范围: tokenURI(默认) | uri 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "https://xxx.ipfs.io/xx/c.json", // token uri, 如为""表示未获取到token uri
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



根据NFT的索引获取TokenID: /nft/tokenid/{index}/{chain}/{protocol} GET


参数:


{index} ≥0的数字, 并且须确保< NFT的totalSupply 必选


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


contract 合约地址 必选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "1032",// token id, 如为""表示未获取到TokenId
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



根据NFT TokenID获取NFT拥有者地址: /nft/ownerof/{tokenId}/{chain}/{protocol} GET


参数:


{tokenId} ≥0的字符串 必选


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


contract 合约地址 必选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "0x345558371fF5d0b7F08066906864318c61f37799",// NFT拥有者地址, 如为""表示未获取到地址
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



根据NFT合约获取NFT发行总量: /nft/totalsupply/{chain}/{protocol} GET


参数:


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


contract 合约地址 必选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body": {
        "content": "3056",// totalSupply, 如为""表示未获取到总量
        "status": "SUCCESS", // FAILED 表示发送交易失败
        "time": 1644749120341
    }
}



根据NFT合约批量获取tokenId、tokenUri、ownerAddress等: /nft/tokenall/{chain}/{protocol} GET Callback


参数:


{chain} 主链名称: eth | bsc | polygon | valar 必选


{protocol} NFT协议，取值范围: erc721 | erc1155 必选


contract 合约地址 必选


param 回调参数, 需URL Encode编码 可选



返回:

{
    "state": 200,
    "msg": "Successful",
    "body":{
        "totalSupply": 0 // 0表示未查询到NFT总量，只有当总量>0时进行批量回调操作
    }
}



Callback Json:

[{
    "chainName": "ETH",
    "protocl": "erc721",
    "contract":"0x0574c34385b039c2bb8db898f61b7767024a9449", // NFT合约地址
    "index":940,   // 合约索引编号
    "tokenId":"941", // token Id
    "owner":"0x46e0dcceb5357f1c59a9de1b29173f85ddb8198f", // owner address
    "url":"https://joyworld.azurewebsites.net/api/HttpTrigger?id\u003d941", // token URI
    "time":1649836589785
}]



扫描某个地址的NFT资产记录: /nft/assets/{chain}/{address} GET Callback


参数:


{chain} 主链名称: eth | bsc | polygon 必选


{address} 钱包地址 必选



返回:

{
    "state": 200,
    "msg": "Successful"
}



Callback Json:

[
  {
    "chainName":"ETH",
    "protocol": "ERC721",
    "address":  "钱包地址",
    "amout":    "该地址持有NFT的数量",
    "name":     "NFT 名称",
    "contract": "NFT 合约", 
    "symbol":   "NFT 符号",
    "tokenIds": ["tokenID", "tokenID"]
  }
]
