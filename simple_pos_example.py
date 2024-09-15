import hashlib
import json
from datetime import datetime
import random

class Block:
    def __init__(self, index, previous_hash, timestamp, data, validator):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_dict = self.__dict__
        if 'hash' in block_dict:
            del block_dict['hash']
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_data = []
        self.validators = {}
        self.staked_tokens = {}
        self.minimum_stake = 10
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, None, str(datetime.now()), "Genesis Block", None)
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def add_data(self, new_data):
        self.unconfirmed_data.append(new_data)

    def add_validator(self, validator, stake):
        if stake >= self.minimum_stake:
            self.staked_tokens[validator] = stake
            self.validators[validator] = True
        else:
            print(f"{validator} does not meet the minimum stake requirement.")
            
    def select_validator(self):
        total_stake = sum(self.staked_tokens.values())
        selected_validator = None
        while selected_validator == None:
            pick = random.uniform(0, total_stake)
            print(pick)
            current = 0
            for validator, stake in self.staked_tokens.items():
                print(validator, stake)
                current += stake
                if current > pick:
                    selected_validator = validator
                    break
        return selected_validator

    def create_block(self, validator):
        if not self.unconfirmed_data:
            return False
        
        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1, 
                          previous_hash=last_block.hash,
                          timestamp=str(datetime.now()),
                          data=self.unconfirmed_data,
                          validator=validator)
        self.chain.append(new_block)
        self.unconfirmed_data = []
        return new_block.index

    def display_chain(self):
        for block in self.chain:
            print(f"Block {block.__dict__}")
            
# Create a Blockchain object
# blockchain = Blockchain()

# Adding some validators
# blockchain.add_validator(999, 10)
# blockchain.add_validator(1111, 50)
# blockchain.add_validator(1222, 30)
# blockchain.add_validator(1333, 20)
# blockchain.add_validator(1444, 20)

# blockchain.add_data("James earned 10 LSU_tokens")
# blockchain.add_data("James pays Mike_the_tiger 5 LSU_tokens")

# selected_validator = blockchain.select_validator()
# print(f"Validator selected: {selected_validator}")

# blockchain.create_block(selected_validator)
# blockchain.display_chain()
