import hashlib
import json
from time import time


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.current_transactions.append(transaction)
        index = self.last_block().index + 1

        return index

    def last_block(self):
        return self.chain.pop()


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
