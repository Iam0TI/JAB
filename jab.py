import time
from hashlib import sha256
import json 


 
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

    def applySha256( self, strinput: str) -> str:
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


   
# a class to  manage a list of blocks 
class Blockchain():
    
    def __init__ (self):
        self.chain = []
        #seting chain diffculty to 6
        self.difficulty = 6
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.chain.append(Block("Genesis Block", "0"))

    def addBlock(self, data):
        previousBlock = self.chain[-1]
        newBlock = Block(data, previousBlock.hash)
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

     #Now we need a way to check the integrity of our blockchain

    def isChainValid(self) -> bool:
        target = '0' * self.difficulty
        #looping thtought blockchain to check hashes
        for i in  range(1,len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i -1]
            #compare registered hash and calculated hash:
            if (currentBlock.hash != currentBlock.calculateHash()):
                print ("Current Hashes not equal")
                return False
            # compare previous hash and registered previous hash
            if ( previousBlock.hash != currentBlock.previousHash):
                print ("Current Hashes not equal")
                return False
            #check if hash is solved
            if (currentBlock.hash[0:self.difficulty] != target ):
                print( "This block hasn't been mined")
                return False
        return True
    
    def toJson(self):
        #using the vars() method to get the __dict__ atribute of an object block 
        return json.dumps([vars(block) for block in self.chain], indent=2)
   
   