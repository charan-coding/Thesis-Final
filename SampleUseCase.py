"""
This is a sample use case, please refer to teh thesis for details
Before running this make sure to create the follwing nodes,

Plese start the nodes,

python Main.py 10001 5001 keys/genesisPrivateKey.pem
python Main.py 10002 5002 keys/stakerPrivateKey.pem
python Main.py 10003 5003 keys/delegate1PrivateKey.pem
python Main.py 10004 5004 keys/delegate2PrivateKey.pem
and then run this file

These are the relevant endpoints,
http://localhost:5001/blockchain - to view the Blockchain
http://localhost:5001/currIssue - to view the Issue Dictinoary
http://localhost:5001/lastForgers - to view the comiled list of previous Forgers
http://localhost:5001/getBalHist - to view the changes in balance (ignore the first entry which is of gensis block)
 
"""


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
    #Wallet Creation
    exchange = Wallet()
    exchange.fromKey('keys/genesisPrivateKey.pem')
    staker = Wallet()
    staker.fromKey('keys/stakerPrivateKey.pem')
    
    delegate1 = Wallet()
    delegate1.fromKey('keys/delegate1PrivateKey.pem')
    delegate2 = Wallet()
    delegate2.fromKey('keys/delegate2PrivateKey.pem')
    
    expert1 = Wallet()
    expert1.fromKey('keys/expert1PrivateKey.pem')
    expert2 = Wallet()
    expert2.fromKey('keys/expert2PrivateKey.pem')
    expert3 =Wallet()
    expert3.fromKey('keys/expert3PrivateKey.pem')
    
    voter1 = Wallet()
    voter1.fromKey('keys/voter1PrivateKey.pem')
    voter2 = Wallet()
    voter2.fromKey('keys/voter2PrivateKey.pem')
    voter3 =Wallet()
    voter3.fromKey('keys/voter3PrivateKey.pem')
    
    alice=Wallet()
    bob = Wallet()

    


    # # forger: genesis
    print("1")
    print(postTransaction(exchange, delegate1, 100, 'EXCHANGE'))
    print(postTransaction(exchange, delegate1, 100, 'EXCHANGE'))
    print(postTransaction(exchange, staker, 106, 'EXCHANGE'))



    print("2")
    print(postTransaction(staker, staker, 5, 'STAKE'))
    print(postTransaction(staker, delegate1, 50, 'TRANSACTION'))
    print(postTransaction(staker, delegate1, 1, 'TRANSACTION'))

    # forger: probably staker
    print("3")
    print(postTransaction(delegate1, delegate1, 104, 'BUYINFIRST'))
    print(postTransaction(exchange, staker, 100, 'EXCHANGE'))
    print(postTransaction(exchange, staker, 100, 'EXCHANGE'))

    
    url = "http://localhost:5001/currIssue"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    out=list(json.loads(response.text).keys())
    print(out[0])
    iss_id=out[0]
    #Get issue id
    

    print("4")
    print(postTransaction(exchange, delegate2, 201, 'EXCHANGE'))
    print(postTransaction(exchange, delegate2, 202, 'EXCHANGE'))
    
    tag={"issue_id": iss_id, "stance": 1}
    print(postTransaction(delegate2, delegate2, 106, 'BUYIN',tag))
    

    
    print("5")
    print(postTransaction(voter1,voter1, 0, 'VOTE',tag))
    print(postTransaction(voter2, voter2, 0, 'VOTE',tag))
    
    tag={"issue_id": iss_id, "stance": 0}
    print(postTransaction(voter3, voter3, 0, 'VOTE',tag))
    

    print("6")
    print(postTransaction(exchange, alice, 203, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 204, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 205, 'EXCHANGE'))
    
    tag={"issue_id": iss_id}
    

    print("7")
    print(postTransaction(expert1, expert1, 0, 'SUGGEST',tag))
    print(postTransaction(expert2, expert2, 0, 'SUGGEST',tag))
    print(postTransaction(expert3, expert3, 0, 'SUGGEST',tag))
    
    print("8")
    print(postTransaction(exchange, alice, 206, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 207, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 208, 'EXCHANGE'))
    
    tag={"issue_id": iss_id}
    
    print("9")   
    print(postTransaction(voter1, expert1, 0, 'EXPERT-VOTE',tag))
    print(postTransaction(voter2, expert2, 0, 'EXPERT-VOTE',tag))
    print(postTransaction(voter3, expert3, 0, 'EXPERT-VOTE',tag))
    
    print("10")
    print(postTransaction(exchange, bob, 209, 'EXCHANGE'))
    print(postTransaction(exchange, bob, 210, 'EXCHANGE'))
    print(postTransaction(exchange, bob, 211, 'EXCHANGE'))
    
    print("11")
    
    tag={"issue_id": iss_id, "stance": 1}
    print(postTransaction(voter1, voter1, 0, 'FINAL-VOTE',tag))
    
    tag={"issue_id": iss_id, "stance": 0}
    print(postTransaction(voter2, voter2, 0, 'FINAL-VOTE',tag))
    print(postTransaction(voter3, voter3, 0, 'FINAL-VOTE',tag))
    
    tag={"issue_id": iss_id, "stance": 1}
    print("12")
    print(postTransaction(expert1, expert1, 0, 'FINAL-VOTE',tag))
    
    tag={"issue_id": iss_id, "stance": 0}
    print(postTransaction(expert2, expert2, 0, 'FINAL-VOTE',tag))
    print(postTransaction(expert3, expert3, 0, 'FINAL-VOTE',tag))
    
    print("13")
    print(postTransaction(exchange, bob, 301, 'EXCHANGE'))
    print(postTransaction(exchange, bob, 302, 'EXCHANGE'))
    print(postTransaction(exchange, bob, 303, 'EXCHANGE'))
    print("14")
    print(postTransaction(exchange, alice, 304, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 305, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 306, 'EXCHANGE'))
    print("15")
    print(postTransaction(exchange, alice, 307, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 308, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 309, 'EXCHANGE'))
    print("16")
    print(postTransaction(exchange, alice, 310, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 311, 'EXCHANGE'))
    print(postTransaction(exchange, alice, 312, 'EXCHANGE'))
    
    