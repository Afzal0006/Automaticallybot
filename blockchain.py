from web3 import Web3
import config, json

w3 = Web3(Web3.HTTPProvider(config.BSC_RPC))

erc20_abi = json.loads("""[
  {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
   "name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
  {"constant":true,"inputs":[{"name":"_owner","type":"address"}],
   "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}
]""")

usdt = w3.eth.contract(address=config.USDT_CONTRACT, abi=erc20_abi)

def verify_payment(tx_hash, expected_amount):
    tx = w3.eth.get_transaction_receipt(tx_hash)
    if not tx: return False

    for log in tx["logs"]:
        if log["address"].lower() == config.USDT_CONTRACT.lower():
            if tx["to"].lower() == config.ESCROW_ADDRESS.lower():
                return True
    return False

def release_funds(to_address, amount, decimals=18):
    nonce = w3.eth.get_transaction_count(config.ESCROW_ADDRESS)
    tx = usdt.functions.transfer(
        Web3.to_checksum_address(to_address),
        int(amount * 10**decimals)
    ).build_transaction({
        "chainId": config.CHAIN_ID,
        "gas": 200000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
    })

    signed_tx = w3.eth.account.sign_transaction(tx, config.ESCROW_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()
