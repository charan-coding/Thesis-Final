from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake
import uuid
import hashlib
import random
from collections import Counter

class Blockchain():

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake(self)

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block):
        #called when receiveing a block, to check if blockcount is valid
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False
        
    def poSHashValid(self, block):
        #called when receiveing a block, to check if posHash is valid
        if self.pos.hashlist[-1] == block.posHash:
            return True
        else:
            return False
        
    def accHashValid(self, block):
        #called when receiveing a block, to check if accHash is valid
        if self.accountModel.hashlist[-1] == block.accHash:
            return True
        else:
            return False

    def lastBlockHashValid(self, block):
        #called when receiveing a block, to check if last block Hash is valid
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        if latestBlockchainBlockHash == block.lastHash:
            return True
        else:
            return False

    def getCoveredTransactionSet(self, transactions):
        #returns valid transactions which pass checks
        coveredTransactions = []
        senderbalances={}
        for transaction in transactions:
            senderbalances[transaction.senderPublicKey]=self.accountModel.getBalance(transaction.senderPublicKey)
            
        for transaction in transactions:
            if self.transactionCovered(transaction, senderbalances):
                coveredTransactions.append(transaction)
        return coveredTransactions

    def transactionCovered(self, transaction, senderbalances):
        #returns true if transaction passes all checks associated with transaction type
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        
        
        
        if transaction.type == 'EXCHANGE':
            if transaction.senderPublicKey==genesisPublicKey:
                return True
            else:
                return False
        elif transaction.type=='RETURN':
            amount = transaction.amount
            receiver = transaction.receiverPublicKey
            if transaction.receiverPublicKey!= transaction.senderPublicKey or receiver not in self.pos.stakers:
                return False
            if amount<=self.pos.get(receiver):
                return True
            else:
                return False
        elif transaction.type=="BUYIN":
            if transaction.receiverPublicKey!= transaction.senderPublicKey or transaction.tag==None or transaction.tag["issue_id"] not in self.pos.currIssueDict.keys() or transaction.amount<=100:
                return False
            else:
                return True
            
        elif transaction.type=="VOTE":
            st=transaction.tag["stance"]
            str1="stance"+str(st)
            
            if transaction.receiverPublicKey!= transaction.senderPublicKey or transaction.tag==None or transaction.tag["issue_id"] not in self.pos.currIssueDict.keys() or transaction.tag["stance"] not in self.pos.currIssueDict[transaction.tag["issue_id"]]["stances"] or self.pos.currIssueDict[transaction.tag["issue_id"]]["stage"] != "INIT-VOTING" or transaction.amount!=0 or transaction.receiverPublicKey in self.pos.currIssueDict[transaction.tag["issue_id"]][str1] :
                return False
            else:
                return True
            
        elif transaction.type=="FINAL-VOTE":
            st=transaction.tag["stance"]
            str1="stance"+str(st)
            
            if transaction.receiverPublicKey!= transaction.senderPublicKey or transaction.tag==None or transaction.tag["issue_id"] not in self.pos.currIssueDict.keys() or transaction.tag["stance"] not in self.pos.currIssueDict[transaction.tag["issue_id"]]["stances"] or self.pos.currIssueDict[transaction.tag["issue_id"]]["stage"] != "FINAL-VOTE" or transaction.amount!=0 or transaction.receiverPublicKey not in self.pos.currIssueDict[transaction.tag["issue_id"]]["all_voters"] :
                return False
            else:
                return True
            
        elif transaction.type=="SUGGEST":
            if transaction.receiverPublicKey!= transaction.senderPublicKey or transaction.tag==None or transaction.tag["issue_id"] not in self.pos.currIssueDict.keys() or transaction.amount!=0:
                return False
            else:
                return True
        elif transaction.type=="EXPERT-VOTE":
            if transaction.tag==None or self.pos.currIssueDict[transaction.tag["issue_id"]]["stage"] != "COUNCIL-VOTE" or transaction.amount!=0 or transaction.receiverPublicKey not in self.pos.currIssueDict[transaction.tag["issue_id"]]["suggested_experts"].keys():
                return False
            else:
                return True
            
        if transaction.type == 'STAKE':
            if transaction.receiverPublicKey!= transaction.senderPublicKey or transaction.amount>=5:
                return True
            else:
                return False
        else:
            if senderbalances[transaction.senderPublicKey] >= transaction.amount:
                senderbalances[transaction.senderPublicKey]-=transaction.amount
                return True
            else:
                return False
            

        

    def executeTransactions(self, transactions):
        self.pos.updateHashlist()
        self.accountModel.updateHashlist()
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        #adds stake
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.pos.update(sender, amount)
            self.accountModel.updateBalance(sender, -amount)
        #Returns stake to user
        elif transaction.type=='RETURN':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.pos.update(receiver, -amount)
            self.accountModel.updateBalance(receiver, amount)
        #Adds user to issue     
        elif transaction.type=='BUYIN':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            details={}
            details["issue_id"]=transaction.tag["issue_id"]
            details["stance"] = transaction.tag["stance"]  
                            
            str1="stance"+str(transaction.tag["stance"])
            str2="finalvote"+str(transaction.tag["stance"])
            str3="delegates"+str(transaction.tag["stance"])
            if transaction.tag["stance"] not in self.pos.currIssueDict[transaction.tag["issue_id"]]["stances"]:
                self.pos.currIssueDict[transaction.tag["issue_id"]]["stances"]+=[transaction.tag["stance"]]
                self.pos.currIssueDict[transaction.tag["issue_id"]][str1]=[receiver]
                self.pos.currIssueDict[transaction.tag["issue_id"]][str2]=[receiver]
                self.pos.currIssueDict[transaction.tag["issue_id"]][str3]=[receiver]
            else:
                self.pos.currIssueDict[transaction.tag["issue_id"]][str1]+=[receiver]
                self.pos.currIssueDict[transaction.tag["issue_id"]][str2]+=[receiver]
                self.pos.currIssueDict[transaction.tag["issue_id"]][str3]+=[receiver]
                    
            self.pos.currIssueDict[transaction.tag["issue_id"]]["blockCount"]=self.blocks[-1].blockCount
            self.pos.currIssueDict[transaction.tag["issue_id"]]["stage"]="INIT-VOTING"
            
            details["amount"]=amount      
            self.pos.currDelegates[receiver]=details

            self.accountModel.updateBalance(receiver, -amount)
                    
        elif transaction.type=='VOTE':
            #registers initial vote
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            str1="stance"+str(transaction.tag["stance"])
            self.pos.currIssueDict[transaction.tag["issue_id"]][str1]+=[receiver]
            self.pos.currIssueDict[transaction.tag["issue_id"]]["all_voters"]+=[receiver]
            
        elif transaction.type=='FINAL-VOTE':
            #registers final vote
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            details=transaction.tag
            if sender not in self.pos.currIssueDict[transaction.tag["issue_id"]]["council"]:
                str1="finalvote"+str(transaction.tag["stance"])
                self.pos.currIssueDict[transaction.tag["issue_id"]][str1]+=[receiver]
                self.pos.currIssueDict[transaction.tag["issue_id"]]["all_voters"].remove(receiver)
            else:
                self.pos.currIssueDict[transaction.tag["issue_id"]]["council_votes"][receiver]=transaction.tag["stance"]
                self.pos.currIssueDict[transaction.tag["issue_id"]]["all_voters"].remove(receiver)
            
        elif transaction.type=='SUGGEST':
            #Suggests experts
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                self.pos.currIssueDict[transaction.tag["issue_id"]]["suggested_experts"][receiver]=0
                
        
        elif transaction.type=='EXPERT-VOTE':
            #Registers expert vote
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            self.pos.currIssueDict[transaction.tag["issue_id"]]["suggested_experts"][receiver]+=1
            self.pos.currIssueDict[transaction.tag["issue_id"]]["all_voters"]+=[receiver]

        elif transaction.type=='BUYINFIRST':
            
            #Creates issue
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            
            latestBlockchainBlockHash1 = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()

            seed = int(latestBlockchainBlockHash1, 16)

            random.seed(seed)
            random_bytes = bytes(random.getrandbits(8) for _ in range(16))
            
            iss_id = str(uuid.UUID(bytes=random_bytes))

            amount = transaction.amount
            details={}
            if amount>=100:
                self.pos.currIssueDict[iss_id]={"stances":[0],"delegates0":[receiver],"stance0":[receiver],"finalvote0":[receiver],
                                                "suggested_experts":{},"all_voters":[], "council":[],"council_votes":{}}
                self.pos.currIssueDict[iss_id]["blockCount"]=self.blocks[-1].blockCount
                self.pos.currIssueDict[iss_id]["stage"]="CREATED"
                details["amount"]=amount
                details["issue_id"]=iss_id
                details["stance"]=0
                self.pos.currDelegates[receiver]=details
                self.accountModel.updateBalance(receiver, -amount)

        else:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)
            self.accountModel.updateBalance(receiver, amount)

    def nextForger(self):
        #calls the pos forger function
        lastBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        self.issue_stage()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger
    
    def issue_stage(self):
        #checks if issue stage needs changing
        for i in self.pos.currIssueDict.keys():
            if self.blocks[-1].blockCount-self.pos.currIssueDict[i]["blockCount"]==2 and self.pos.currIssueDict[i]["stage"]== "INIT-VOTING":
                self.pos.currIssueDict[i]["stage"]="COUNCIL-SUGGEST"
                self.pos.currIssueDict[i]["blockCount"]=self.blocks[-1].blockCount
            if self.blocks[-1].blockCount-self.pos.currIssueDict[i]["blockCount"]==2 and self.pos.currIssueDict[i]["stage"]== "COUNCIL-SUGGEST":
                self.pos.currIssueDict[i]["stage"]="COUNCIL-VOTE"
                self.pos.currIssueDict[i]["blockCount"]=self.blocks[-1].blockCount
            if self.blocks[-1].blockCount-self.pos.currIssueDict[i]["blockCount"]==2 and self.pos.currIssueDict[i]["stage"]== "COUNCIL-VOTE":
                self.addToCouncil(i)
                self.pos.currIssueDict[i]["stage"]="FINAL-VOTE"
                self.pos.currIssueDict[i]["blockCount"]=self.blocks[-1].blockCount
            if self.blocks[-1].blockCount-self.pos.currIssueDict[i]["blockCount"]==3 and self.pos.currIssueDict[i]["stage"]== "FINAL-VOTE":
                self.finalVoteProcess(i)
                self.reward(i)
                self.pos.currIssueDict[i]["stage"]="FINISHED"
                self.pos.currIssueDict[i]["blockCount"]=self.blocks[-1].blockCount

    def createBlock(self, transactionsFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(
            transactionsFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(
            coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks),self.pos.hashlist[-2],self.accountModel.hashlist[-2])
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction):
        #checks if received transactions are in pool
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block):
        #checks if user who broadcasted block is the forger
        forgerPublicKey = self.pos.previousForgers[len(self.pos.previousForgers)-1]
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
    
    def addToCouncil(self, i):
        for expert_id in self.pos.currIssueDict[i]["suggested_experts"].keys():
            if self.pos.currIssueDict[i]["suggested_experts"][expert_id]>=1:
                self.pos.currIssueDict[i]["council"]+=[expert_id]
    
    def finalVoteProcess(self,iss_id):
        
        #final vote process check the disseration for details
        all_voters=[]
        for temp in self.pos.currIssueDict[iss_id]["stances"]:
            str1="finalvote"+str(temp)
            all_voters+=self.pos.currIssueDict[iss_id][str1]
        council_voters=list(self.pos.currIssueDict[iss_id]["council_votes"].keys())
        self.pos.currIssueDict[iss_id]["bootstrapped_voting_results"]={}
        winning_stances=[]
        self.pos.currIssueDict[iss_id]["all_voter_check"]=all_voters
        round=1
        while len(all_voters)!=0:
            lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
            hash_seed = int(lastBlockHash, 16) % (10 ** 8)
            random.seed(hash_seed)
            selected_voters=[]
            if len(all_voters)>1:
                selected_voters.extend(random.sample(all_voters, 2))
                all_voters = [item for item in all_voters if item not in selected_voters]
                selected_voters.extend(random.sample(council_voters, 1))
            else:
                selected_voters.extend(random.sample(all_voters, 1))
                all_voters=[]
                selected_voters.extend(random.sample(council_voters, 2))
            winning_stances+=self.bootstrapped_voting_round(selected_voters, iss_id, hash_seed, round)
            round+=1
        
        self.pos.currIssueDict[iss_id]["winning_stances"]=winning_stances
        stance_counts = Counter(winning_stances)
        max_occurrence = max(stance_counts.values())
        final_winner = [stance for stance, count in stance_counts.items() if count == max_occurrence]
        self.pos.currIssueDict[iss_id]["Final_winner"]=random.sample(final_winner,1)
            
        
    def bootstrapped_voting_round(self,selected_voters, iss_id, hash_seed,round):
        #part of the final vote process check the disseration for details
        stanceDict={}
        for stance in self.pos.currIssueDict[iss_id]["stances"]:
            stanceDict[stance]=0
        for voter in selected_voters:
            weight=self.accountModel.getWeight(voter)
            for stance in self.pos.currIssueDict[iss_id]["stances"]:
                str1="finalvote"+str(stance)
                if voter in self.pos.currIssueDict[iss_id][str1]:
                    stanceDict[stance]+=weight
            if voter in self.pos.currIssueDict[iss_id]["council"]:
                stanceDict[self.pos.currIssueDict[iss_id]["council_votes"][voter]]+=weight
        
        max_votes = max(stanceDict.values())
        winners = [stance for stance, votes in stanceDict.items() if votes == max_votes]
        self.pos.currIssueDict[iss_id]["bootstrapped_voting_results"][round]={"voters":selected_voters,"stances":stanceDict}
        random.seed(hash_seed)
        return random.sample(winners,1)
    
    def reward(self, iss_id):
        #reward funciton actual incentivization
        Alpha=4#incentive constant
        winning_stance=self.pos.currIssueDict[iss_id]["Final_winner"][0]
        winner_delegates=self.pos.currIssueDict[iss_id]["delegates"+str(winning_stance)]
        self.pos.delegateWinners+=winner_delegates
        total_winnings=0
        total_winning_stake=0
        current_delegates=self.pos.currDelegates
        for delegate in current_delegates.keys():
            if self.pos.currDelegates[delegate]["issue_id"]==iss_id and delegate not in winner_delegates:
                total_winnings+=self.pos.currDelegates[delegate]["amount"]
                self.accountModel.updateWeight(delegate,1/Alpha)
                self.accountModel.participatedIssues[delegate]+=[iss_id]
            elif self.pos.currDelegates[delegate]["issue_id"]==iss_id and delegate in winner_delegates:
                total_winning_stake+=self.pos.currDelegates[delegate]["amount"]
                self.accountModel.updateWeight(delegate,Alpha)
                self.accountModel.updateBalance(delegate,self.pos.currDelegates[delegate]["amount"])
                self.accountModel.participatedIssues[delegate]+=[iss_id]
                
        for winner in winner_delegates:
            delegate_reward = (self.pos.currDelegates[winner]["amount"] / total_winning_stake) * total_winnings
            self.accountModel.updateBalance(winner,delegate_reward)
            
        for council_member in self.pos.currIssueDict[iss_id]["council"]:
            self.accountModel.updateWeight(council_member,Alpha/3)
            self.accountModel.updateBalance(council_member,10)
        
        for temp in self.pos.currIssueDict[iss_id]["stances"]:
            str1="finalvote"+str(temp)
            if temp!=winning_stance:
                for voters in self.pos.currIssueDict[iss_id][str1]:
                    self.accountModel.updateWeight(voters,1/(Alpha/2))
            else:
                for winning_voters in self.pos.currIssueDict[iss_id][str1]:
                    self.accountModel.updateWeight(winning_voters,(Alpha/2))
                
    
            
        
        

            
        
        
        