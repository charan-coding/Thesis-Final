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
    delegate1 = Wallet()
    delegate1.fromKey('keys/delegate1PrivateKey.pem')
    staker = Wallet()
    staker.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()
    exchange.fromKey('keys/genesisPrivateKey.pem')


    # # forger: genesis
    print(postTransaction(exchange, delegate1, 100, 'EXCHANGE'))
    print(postTransaction(exchange, delegate1, 100, 'EXCHANGE'))
    print(postTransaction(exchange, staker, 56, 'EXCHANGE'))


    # forger: probably staker
    
    print(postTransaction(staker, staker, 5, 'STAKE'))
    print(postTransaction(staker, delegate1, 50, 'TRANSACTION'))
    print(postTransaction(staker, delegate1, 1, 'TRANSACTION'))


    print(postTransaction(delegate1, delegate1, 104, 'BUYINFIRST'))
    print(postTransaction(exchange, staker, 100, 'EXCHANGE'))
    print(postTransaction(exchange, staker, 100, 'EXCHANGE'))
