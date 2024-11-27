import uuid
import time
import copy


class Transaction():

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type, tag=None):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = (uuid.uuid1()).hex
        self.timestamp = time.time()
        self.signature = ''
        if self.type=="BUYIN" or self.type=="VOTE" or self.type=="SUGGEST" or self.type=="FINAL-VOTE" or self.type=="EXPERT-VOTE":
            self.tag = tag

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False
