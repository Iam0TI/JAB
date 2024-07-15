from block import Block
import json 

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
        #looping through blockchain to check hashes
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
   
   