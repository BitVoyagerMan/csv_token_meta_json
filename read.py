import csv
import json
import requests
from web3 import Web3, HTTPProvider
from urllib.parse import urlparse
file = open("data.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
data = [row[0] for row in data][1:]
file = open("ERC721ABI.json", "r")
abi = json.load(file)['ABI']
file.close()
w3 = Web3(HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/vhgO2iZpWuCCQDMEWcegkkN6sbTPitfs"))
result = {}


for item in data:
    contract = w3.eth.contract(address=Web3.to_checksum_address(item), abi=abi)
    total_supply = contract.functions.totalSupply().call()
    for i in range(total_supply):
        try:
            tokenURI = contract.functions.tokenURI(i+1).call()
            parsed_uri = urlparse(tokenURI)
            
            if parsed_uri.scheme == 'http' or parsed_uri.scheme == 'https':
                tokenURI = parsed_uri
            else:
                tokenURI = 'https://ipfs.io/ipfs/{uri.netloc}/{uri.path}'.format(uri = parsed_uri)
            print(tokenURI)
            response = requests.get(tokenURI)
            tokenDetails = response.json()
            print(tokenDetails)
            result[item][i] = tokenDetails
        except:
            continue
with open("out.json", "w") as outfile:
    json.dump(result, outfile)

# {
#     "address1": {
#         "tokenID1": {},
#         "tokenID2": {},
#         ...
#     }
#     "address2": {
#        "tokenID1": {},
#         "tokenID2": {},
#         ...
#     } 
#     ...
# }
