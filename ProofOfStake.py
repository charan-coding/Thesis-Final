from BlockchainUtils import BlockchainUtils
import random
from AccountModel import AccountModel
from Wallet import Wallet
import requests
import hashlib

class ProofOfStake():

    def __init__(self, chain):
        self.stakers = {}
        self.setGenesisNodeStake()
        self.previousForgers=[]
        self.currIssueDict={}
        self.currDelegates={}
        self.chainCopy=chain
        self.previousIssues={}
        self.currWinners=[]
        self.hashlist=['firsthash','firsthash']
        self.delegateWinners=[]

    def setGenesisNodeStake(self):
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        self.stakers[genesisPublicKey] = 1

    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake
        else:
            self.stakers[publicKeyString] = stake

    def get(self, publicKeyString):
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None
    #creates lots to pick from, dictionary with key and effective stake
    def validatorLots(self):
        effectiveWeight={}
        for validator in self.stakers.keys():
            eff=self.get(validator)*self.chainCopy.accountModel.getWeight(validator)
            effectiveWeight[validator]=eff
        return effectiveWeight
    

    def winnerLot(self, lots, lastBlockHash):
        #chooses winning lot
        hash_seed = int(lastBlockHash, 16) % (10 ** 8)
        random.seed(hash_seed)
        
        total = sum(lots.values())
        normalized_weights = [value / total for value in lots.values()]
        winnerLot = random.choices(list(lots.keys()), weights=normalized_weights, k=1)[0]
        return winnerLot

    def forger(self, lastBlockHash):
        #chooses forger and adds to list of forgers
        if len(self.delegateWinners)==0:
            lots = self.validatorLots()
            winnerLot = self.winnerLot(lots, lastBlockHash)
            self.previousForgers.append(winnerLot)
            self.chainCopy.accountModel.updateBalance(winnerLot, self.stakers[winnerLot]+5)
            del self.stakers[winnerLot]
            self.setGenesisNodeStake()
            return winnerLot
        else:
            hash_seed = int(lastBlockHash, 16) % (10 ** 8)
            random.seed(hash_seed)
            winnerLot = random.choice(self.delegateWinners)  
            self.previousForgers.append(winnerLot)
            self.delegateWinners.remove(winnerLot)
            return winnerLot

    def getStake(self):
        stake={}
        for validator in self.stakers.keys():
            stk=self.get(validator)
            stake[validator]=stk
        return stake
    
    def getWeight(self):
        Weight={}
        for validator in self.stakers.keys():
            wg=self.accountModel.getWeight(validator)
            Weight[validator]=wg
        return Weight
    
    def updateHashlist(self):
        tempDict={}
        tempDict["stakers"]=self.stakers 
        tempDict["previousForgers"]=self.previousForgers
        tempDict["currIssueDict"]=self.currIssueDict
        tempDict["currDelegates"]=self.currDelegates
        tempDict["previousIssues"]=self.previousIssues
        tempDict["currWinners"]=self.currWinners
        out=BlockchainUtils.hash(tempDict).hexdigest()
        self.hashlist+= [out]