from blockchain import BlockChain
from uuid import uuid4

from flask import Flask, jsonify

bc = BlockChain()
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    pass


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bc.chain,
        'lenght': len(bc.chain)
    }

    return jsonify(response), 200
