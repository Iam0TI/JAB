from string_util import string_util
from merkle import get_merkle_root
from datetime import datetime

 
class Block  :

    #block constructor
    def __init__(self,previousHash:str ) -> None:
        self.previousHash = previousHash
        now = datetime.now()    
        self.timeStamp:int = int(int(now.timestamp())* 1000)
        self.nonce = 0 
        self.transactions = []
        self.merkle_root = self.compute_merkle_root()
        self.hash:str = self.calculate_hash ()
       
        

     #to calculate hash   
    def calculate_hash (self)  -> str :
        # Concatenate the merkle_rooot, previous hash, and timestamp into a single string
        hashString = self.previousHash + str(self.timeStamp) + str(self.nonce) + self.merkle_root
        # Calculate the hash using SHA-256
        return string_util.apply_sha_256(hashString)
    
    def  mine_block(self,difficulty):
        
       self.merkle_root = get_merkle_root(self.transactions)
       target = '0' * difficulty  # Create a string with difficulty * "0"
       while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
       print(f"Block Mined!!! : {self.hash}")


    def compute_merkle_root(self):
        transaction_ids = [tx.transaction_id for tx in self.transactions]
        return get_merkle_root(transaction_ids)

    def add_transaction(self, transaction,blockchain) -> bool:
        #process transaction and check if valid, unless block is genesis block then ignore.
        if transaction is None:
            return False
        
        if (self.previousHash != "0"):
            if not transaction.process_transaction(blockchain) :
                print("Transaction failed to process. Discarded.")
                return False
            
        self.transactions.append(transaction)
        print("Transaction Successfully added to Block")
        return True
        