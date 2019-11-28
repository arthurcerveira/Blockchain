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

        # Genesis block
        self.new_block()

    def new_block(self, proof=100, previous_hash='1'):
        index = len(self.chain) + 1

        block = Block(index, self.current_transactions, proof, previous_hash)

        self.current_transactions = []
        self.chain.append(block)

        return block

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
        return self.chain[-1]

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
        first_block = True
        last_block = None

        for block_dict in chain:
            if first_block is True:
                last_block = self.dict_to_block(block_dict)
                first_block = False
                continue

            block = self.dict_to_block(block_dict)

            if block.previous_hash != last_block.hash():
                return False

            if not self.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block

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
            new_chain = list(map(lambda x: self.dict_to_block(x), new_chain))
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()

        return block_hash

    @staticmethod
    def dict_to_block(dictionary):
        return Block(dictionary["index"],
                     dictionary["transactions"],
                     dictionary["proof"],
                     dictionary["previous_hash"])


class Block(object):
    def __init__(self, index=0, transactions=None, proof=100, previous_hash='1'):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def hash(self):
        block_dict = self.__dict__

        block_string = json.dumps(block_dict, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()

        return block_hash
