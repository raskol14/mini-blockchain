import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}..., prev={self.previous_hash[:10]}...)"

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3  # başta kolay olsun

    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        # hash'in başında difficulty kadar 0 olacak
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time(),
            data=data,
            previous_hash=last_block.hash
        )
        mined_block = self.proof_of_work(new_block)
        self.chain.append(mined_block)
        return mined_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # hash doğru mu
            if current.hash != current.calculate_hash():
                return False

            # previous hash bağlantısı doğru mu
            if current.previous_hash != previous.hash:
                return False

        return True

if __name__ == "__main__":
    bc = Blockchain()
    print("⛏ Blok kazılıyor...")
    bc.add_block({"from": "alice", "to": "bob", "amount": 10})
    print("⛏ Blok kazılıyor...")
    bc.add_block({"from": "bob", "to": "carol", "amount": 3})

    for block in bc.chain:
        print(block)

    print("Zincir geçerli mi?", bc.is_chain_valid())
