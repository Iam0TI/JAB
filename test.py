import simplejson as json
import time as time
from block import Block,Blockchain


start = time.time() 
# Create a Blockchain instance
blockchain = Blockchain()

# Add blocks to the blockchain
blockchain.addBlock("Hi im the first block")
blockchain.addBlock("Yo im the second block")
blockchain.addBlock("Hey im the third block")
blockchain.addBlock("Heyy im the fourth block")


# Convert blockchain to JSON format
blockchainJson = blockchain.toJson()

# Print JSON representation of the blockchain
print(blockchainJson)
print(blockchain.isChainValid())
#print(blockchain.())
end = time.time() 
print(f"Time elapsed during the calculation:{end - start}")     