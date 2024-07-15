import time
from hashlib import sha256

 
class Block  :

    #block constructor
    def __init__(self, data:str , previousHash:str ) -> None:
        self.data = data
        self.previousHash = previousHash
        self.timeStamp:int = int(time.time() * 1000)
        self.nonce = 0 
        self.difficulty = 6
        self.hash:str = self.calculateHash ()
        


    #Applies Sha256 to a string and returns the result. 

    def apply_sha_256( self, strinput: str) -> str:
        try:
            hash :str = sha256(strinput.encode('utf-8')).hexdigest()
            return hash 
        except Exception as e: 
            raise RuntimeError(e)

  
     #to calculate hash   
    def calculateHash (self)  -> str :
        # Concatenate the data, previous hash, and timestamp into a single string
        hashString = self.data + self.previousHash + str(self.timeStamp) + str(self.nonce)
        # Calculate the hash using SHA-256
        return self.applySha256(hashString)
    
    def mineBlock(self, difficulty:int):
        
       target = '0' * difficulty  # Create a string with difficulty * "0"
       while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculateHash()
        
       print(f"Block Mined!!! : {self.hash}")


   
