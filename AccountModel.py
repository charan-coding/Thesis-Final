from BlockchainUtils import BlockchainUtils
class AccountModel():

    def __init__(self):
        self.accounts = []
        self.balances = {}
        self.weight={}
        self.participatedIssues={}
        self.balance_history={}
        self.weight_history={}
        self.hashlist=['firsthash','firsthash']

    def addAccount(self, publicKeyString):
        #initialize account
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0
            self.weight[publicKeyString]=1
            self.participatedIssues[publicKeyString]=[]
            self.balance_history[publicKeyString]=[]
            self.weight_history[publicKeyString]=[]
            

    def getBalance(self, publicKeyString):
        #retreive balance
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]
    
    def getBalanceHist(self):
        #retreive history of change in balances
        return self.balance_history

    def updateBalance(self, publicKeyString, amount):
        #Change balance
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balance_history[publicKeyString]+=[amount]
        self.balances[publicKeyString] += amount
        
    def getWeight(self, publicKeyString):
        #retreive Weight
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.weight[publicKeyString]
    
    def updateWeight(self, publicKeyString, change):
        #Change weight
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.weight_history[publicKeyString]+=[change]
        self.weight[publicKeyString]*=change

    def updateHashlist(self):
        #Create and Updtae hash of current state
        tempDict={}
        tempDict["Weight History"]=self.weight_history
        tempDict["Balancce History"]=self.balance_history
        tempDict["Issues participated"]=self.participatedIssues
        out=BlockchainUtils.hash(tempDict).hexdigest()
        self.hashlist+= [out]