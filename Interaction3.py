from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
import json


def postTransaction(sender, receiver, amount, type, tag=None):
    if type=="BUYIN" or type=="VOTE" or type=="SUGGEST" or type=="FINAL-VOTE" or type=="EXPERT-VOTE":
        transaction = sender.createTransaction(
            receiver.publicKeyString(), amount, type,tag)
    else:
        transaction = sender.createTransaction(
            receiver.publicKeyString(), amount, type)
    url = "http://localhost:5001/transaction"
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)



if __name__ == '__main__':
    
    url = "http://localhost:5001/currIssue"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    out=list(json.loads(response.text).keys())
    print(out[0])
    iss_id=out[0]
    
    alice = Wallet()
    exchange = Wallet()
    exchange.fromKey('keys/genesisPrivateKey.pem')
    
    tag={"issue_id": iss_id}
    
    
    expert1 = Wallet()
    expert1.fromKey('keys/expert1PrivateKey.pem')
    expert2 = Wallet()
    expert2.fromKey('keys/expert2PrivateKey.pem')
    expert3 =Wallet()
    expert3.fromKey('keys/expert3PrivateKey.pem')
    
    print(postTransaction(expert1, expert1, 0, 'SUGGEST',tag))
    print(postTransaction(expert2, expert2, 0, 'SUGGEST',tag))
    print(postTransaction(expert3, expert3, 0, 'SUGGEST',tag))
    
    
    print(postTransaction(exchange, alice, 206, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 207, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 208, 'EXCHANGE'))
    
    
