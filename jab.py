import time
from hashlib import sha256


  #  function to generate digital fingerprint 

class Block  :

    #block constructor
    def __init__(self, data:str , previousHash:str ) -> None:
        self.data = data
        self.previousHash = previousHash
        self.timeStamp:int = int(time.time() * 1000)
        self.hash:str = self.calculateHash ()



    def applySha256( self, strinput: str) -> str:
        try:
            hash :str = sha256(strinput.encode('utf-8')).hexdigest()
            return hash 
        except Exception as e: 
            raise RuntimeError(e)

  
        
    def calculateHash (self)  -> str :
        # Concatenate the data, previous hash, and timestamp into a single string
        hashString = self.data + self.previousHash + str(self.timeStamp)
        # Calculate the hash using SHA-256
        return self.applySha256(hashString)
   


genesisBlock =  Block("Hi im the first block", "0")
print(f" Hash for block1 : {genesisBlock.hash}")
secondBlock =  Block("Hi im the second block", genesisBlock.hash)
print(f" Hash for block 2 : {secondBlock.hash}")
thridBlock =  Block("Hi im the thrid block", secondBlock.hash)
print(f" Hash for block 3: {thridBlock.hash}")
            