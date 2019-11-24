import hashlib
import json
from time import time

VERIFY_KEY = "0000"


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

        return transaction

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
