from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

node = None
#api class with diffferent end points


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=port)

    def injectNode(self, injectedNode):
        global node
        node = injectedNode

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communiction interface to a nodes blockchain', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200

    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
    
    @route('/stakes', methods=['GET'])
    def stakes(self):
        output=node.blockchain.accountModel.getStake()
        return jsonify(output), 200
    
    @route('/weights', methods=['GET'])
    def weights(self):
        output=node.blockchain.accountModel.getWeight()
        return jsonify(output), 200
    
    @route('/effstake', methods=['GET'])
    def effstake(self):
        output=node.blockchain.pos.validatorLots()
        return jsonify(output), 200
    
    @route('/getBalBackup', methods=['GET'])
    def getBalBackup(self):
        output={}
        keys=node.blockchain.accountModel.accounts
        for publicKey in keys:
            output[publicKey]=node.blockchain.accountModel.getBalance(publicKey)
        return jsonify(output), 200
    
    @route('/getBal', methods=['GET'])
    def getBal(self):
        keys=node.blockchain.accountModel.accounts
        output=dict(map(lambda key: (key, node.blockchain.accountModel.getBalance(key)), keys))
        return jsonify(output), 200
    
    @route('/lastForgers', methods=['GET'])
    def lastFogers(self):
        output=node.blockchain.pos.previousForgers
        return jsonify(output), 200
    
    @route('/currIssue', methods=['GET'])
    def currIssue(self):
        output=node.blockchain.pos.currIssueDict
        return jsonify(output), 200
    
    @route('/currDelegate', methods=['GET'])
    def currDelegate(self):
        output=node.blockchain.pos.currDelegates
        return jsonify(output), 200
    
    @route('/getBalHist', methods=['GET'])
    def getBalHist(self):
        output=node.blockchain.accountModel.getBalanceHist()
        return jsonify(output), 200
    
    @route('/getWeightHist', methods=['GET'])
    def getWeightHist(self):
        output=node.blockchain.accountModel.weight_history
        return jsonify(output), 200
    
    @route('/getPoSHashList', methods=['GET'])
    def getPoSHashList(self):
        output=node.blockchain.pos.hashlist
        return jsonify(output), 200