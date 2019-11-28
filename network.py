from blockchain import BlockChain
from uuid import uuid4
import sys

from flask import Flask, jsonify, request

bc = BlockChain()
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    # Brute force the next proof
    last_block = bc.last_block()
    last_proof = last_block.proof
    proof = bc.proof_of_work(last_proof)

    # Perform a new transaction with the proof
    bc.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1
    )

    # Generate a new block
    previous_hash = last_block.hash()
    block = bc.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transaction': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = bc.new_transaction(values['sender'],
                                     values['recipient'],
                                     values['amount'])

    return jsonify(transaction), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    chain = tuple(map(lambda x: x.__dict__, tuple(bc.chain)))
    response = {
        'chain': chain,
        'lenght': len(bc.chain)
    }

    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Invalid list of nodes", 400

    for node in nodes:
        bc.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(bc.nodes)
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = bc.resolve_conflicts()

    if replaced:
        message = 'Our chain was replaced'
    else:
        message = 'Our chain is authoritative'

    chain = tuple(map(lambda x: x.__dict__, tuple(bc.chain)))

    response = {
        'message': message,
        'chain': chain
    }

    return jsonify(response), 200


if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
