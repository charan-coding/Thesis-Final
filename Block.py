import time
import copy


class Block():

    def __init__(self, transactions, lastHash, forger, blockCount, posHash, accHash):
        self.blockCount = blockCount
        self.transactions = transactions
        self.lastHash = lastHash
        self.timestamp = time.time()
        self.forger = forger
        self.signature = ''
        self.posHash=posHash
        self.accHash=accHash

    @staticmethod
    def genesis():
        genesisBlock = Block([], 'genesisHash', 'genesis', 0,'firstHash','firsthash')
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        data = {}
        data['blockCount'] = self.blockCount
        data['lastHash'] = self.lastHash
        data['signature'] = self.signature
        data['forger'] = self.forger
        data['timestamp'] = self.timestamp
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        data['posHash']=self.posHash
        data['accHash']=self.accHash
        
        return data

    def payload(self):
        
        #payload function for hashing and chekcing hash
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        self.signature = signature
