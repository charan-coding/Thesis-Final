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
    
    delegate2 = Wallet()
    delegate2.fromKey('keys/delegate2PrivateKey.pem')
    exchange = Wallet()
    exchange.fromKey('keys/genesisPrivateKey.pem')

    print(postTransaction(exchange, delegate2, 201, 'EXCHANGE'))
    print(postTransaction(exchange, delegate2, 202, 'EXCHANGE'))
    
    tag={"issue_id": iss_id, "stance": 1}
    print(postTransaction(delegate2, delegate2, 106, 'BUYIN',tag))
    
    voter1 = Wallet()
    voter1.fromKey('keys/voter1PrivateKey.pem')
    voter2 = Wallet()
    voter2.fromKey('keys/voter2PrivateKey.pem')
    voter3 =Wallet()
    voter3.fromKey('keys/voter3PrivateKey.pem')
    
    
    print(postTransaction(voter1,voter1, 0, 'VOTE',tag))
    print(postTransaction(voter2, voter2, 0, 'VOTE',tag))
    
    tag={"issue_id": iss_id, "stance": 0}
    print(postTransaction(voter3, voter3, 0, 'VOTE',tag))
    
    alice=Wallet()
    
    print(postTransaction(exchange, alice, 203, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 204, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 205, 'EXCHANGE'))
    
    
