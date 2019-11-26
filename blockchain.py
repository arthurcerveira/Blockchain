import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

VERIFY_KEY = "0000"


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.current_transactions.append(transaction)

        return transaction

    def register_node(self, address):
        url = urlparse(address)

        self.nodes.add(url.netloc)

    def last_block(self):
        return self.chain.pop()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{ last_proof }{ proof }'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return True if VERIFY_KEY in guess_hash else False

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{ last_block }')
            print(f'{ block }')
            print("\n---------------\n")

            if block.previous_hash != last_block.hash():
                return False

            if not self.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_lenght = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{ node }/chain')

            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']

                if lenght > max_lenght and self.valid_chain(chain):
                    max_lenght = lenght
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False


class Block(object):
    def __init__(self, index, transaction, proof, previous_hash=None):
        self.index = index
        self.timestamp = time()
        self.transaction = transaction
        self.proof = proof
        self.previous_hash = previous_hash

    def hash(self):
        block_string = json.dumps(self, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()

        return block_hash
