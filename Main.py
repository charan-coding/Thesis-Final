from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
import pprint
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys

if __name__ == '__main__':
    ip = "localhost"
    port = int(sys.argv[1])
    apiPort = int(sys.argv[2])
    keyFile = None
    if len(sys.argv) > 3:
        keyFile = sys.argv[3]

    node = Node(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)

