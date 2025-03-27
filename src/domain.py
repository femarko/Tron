import tronpy

client = tronpy.Tron(network="nile")
wallet = client.generate_address()
# client.create_account(wallet["base58check_address"])
# info = client.get_account(wallet["base58check_address"])

bal = client.get_account_balance(addr=str(wallet["base58check_address"]))
pass