from block import Block
import json 
from datetime import datetime
from string_util import string_util

# a class to  manage a list of blocks 
class Blockchain():
    
    def __init__ (self):
        self.chain = []
        self.UTXOs  ={}
        #seting chain diffculty to 6
        self.difficulty =  6
        self.minimum_transaction = 0.1
        self.create_genesis_block()


    def create_genesis_block(self):
        genesis_block = Block("0")  
        self.chain.append(genesis_block)
    
        


    def add_block(self, new_block):
        if len(self.chain) > 0:
            new_block.previousHash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        # update UTXOs based on the transactions in the new block
        self.update_UTXOs(new_block)


     
    def get_latest_block(self):
        return self.chain[-1]
    
    def update_UTXOs(self, block):
        for tx in block.transactions:
            # remove spent outputs
            for input in tx.inputs:
                self.UTXOs.pop(input.transaction_output_id, None)
            
            # add new unspent outputs
            for output in tx.outputs:
                self.UTXOs[output.id] = output

    def get_UTXO(self, utxo_id):
        return self.UTXOs.get(utxo_id)

    def is_UTXO_valid(self, utxo_id):
        return utxo_id in self.UTXOs
    
    def get_balance(self, public_key):
        balance = 0
        for utxo in self.UTXOs.values():
            if utxo.is_mine(public_key):
                balance += utxo.value
        return balance

    #Now we need a way to check the integrity of our blockchain
    def is_chain_valid(self):
        hash_target = '0' * self.difficulty
        temp_UTXOs = {}
        
       
        # loop through blockchain to check hashes:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # compare registered hash and calculated hash:
            if current_block.hash != current_block.calculate_hash():
                print("#current hashes not equal")
                return False
            
            # compare previous hash and registered previous hash
            if previous_block.hash != current_block.previousHash:
                print("#previous hashes not equal")
                return False
            
            # check if hash is solved
            if current_block.hash[:self.difficulty] != hash_target:
                print("#this block hasn't been mined")
                return False

            # loop through block transactions:
            for t, current_transaction in enumerate(current_block.transactions):
                if not current_transaction.verify_signature():
                    print(f"#signature on transaction({t}) is invalid")
                    return False
                
                if current_transaction.get_inputs_value() != current_transaction.get_outputs_value():
                    print(f"#inputs are not equal to outputs on transaction({t})")
                    return False
                
                for input in current_transaction.inputs:
                    temp_output = temp_UTXOs.get(input.transaction_output_id)
                    if temp_output is None:
                        print(f"#referenced input on transaction({t}) is missing")
                        return False
                    
                    if input.UTXO.value != temp_output.value:
                        print(f"#referenced input transaction({t}) value is invalid")
                        return False
                    
                    del temp_UTXOs[input.transaction_output_id]
                
                for output in current_transaction.outputs:
                    temp_UTXOs[output.id] = output
                
                if current_transaction.outputs[0].recipient != current_transaction.recipient:
                    print(f"#transaction({t}) output recipient is not who it should be")
                    return False
                
                if len(current_transaction.outputs) > 1 and current_transaction.outputs[1].recipient != current_transaction.sender:
                    print(f"#transaction({t}) output 'change' is not sender.")
                    return False

        print("blockchain is valid")
        return True


    def print_blockchain(self):
        print("\n=== Blockchain ===")
        for i, block in enumerate(self.chain):
            print(f"\nBlock {i}:")
            print(f"  Timestamp: {datetime.fromtimestamp(block.timeStamp / 1000)}")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previousHash}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Merkle Root: {block.merkle_root}")
            print("  Transactions:")
            for tx in block.transactions:
                print(f"    - From: {tx.sender[:10]}... To: {tx.recipient[:10]}... Amount: {tx.value}")
        
        print("\n=== UTXO Set ===")
        for utxo_id, utxo in self.UTXOs.items():
            print(f"  UTXO {utxo_id[:10]}... : Recipient: {utxo.recipient[:10]}... Value: {utxo.value}")

    def to_json(self):
        blockchain_dict = {
            "chain": [self._block_to_dict(block) for block in self.chain],
            "UTXOs": {utxo_id: self._utxo_to_dict(utxo) for utxo_id, utxo in self.UTXOs.items()},
            "difficulty": self.difficulty,
            "minimum_transaction": self.minimum_transaction
        }
        return json.dumps(blockchain_dict, indent=2)

    def _block_to_dict(self, block):
        return {
            "hash": block.hash,
            "previousHash": block.previousHash,
            "timeStamp": block.timeStamp,
            "nonce": block.nonce,
            "merkle_root": block.merkle_root,
            "transactions": [self._transaction_to_dict(tx) for tx in block.transactions]
        }

    def _transaction_to_dict(self, tx):
        return {
            "transaction_id": tx.transaction_id,
            "sender": string_util.get_string_from_key(tx.sender),
            "recipient": string_util.get_string_from_key(tx.recipient),
            "value": tx.value,
            "inputs": [{"transaction_output_id": input.transaction_output_id} for input in tx.inputs],
            "outputs": [self._utxo_to_dict(output) for output in tx.outputs]
        }

    def _utxo_to_dict(self, utxo):
        return {
            "id": utxo.id,
            "recipient": string_util.get_string_from_key(utxo.recipient),
            "value": utxo.value,
            "parent_transaction_id": utxo.parent_transaction_id
        }
   
   