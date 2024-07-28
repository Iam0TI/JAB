from wallet import Wallet
from blockchain import Blockchain
from transaction import Transaction, TransactionOutput
from block import Block

def main():
     
    blockchain = Blockchain()

    walletA = Wallet(blockchain)
    walletB = Wallet(blockchain)
    coinbase = Wallet(blockchain)

    # Create genesis transaction, which sends 100 NoobCoin to walletA
    genesis_transaction = Transaction(coinbase.public_key, walletA.public_key, 100, [])
    genesis_transaction.generate_signature(coinbase.private_key) 
    genesis_transaction.transaction_id = "0"  
    print("\ncoinbase's balance is:", coinbase.get_balance())
    genesis_transaction.outputs.append(TransactionOutput(genesis_transaction.recipient, genesis_transaction.value, genesis_transaction.transaction_id))  
    blockchain.UTXOs[genesis_transaction.outputs[0].id] = genesis_transaction.outputs[0]  # store the first transaction in the UTXOs list

    print("Creating and Mining Genesis block... ")
    genesis_block = Block("0")
    blockchain.add_block(genesis_block)

    # testing ....
    block1 = Block( blockchain.get_latest_block().hash)
    print("\nWalletA's balance is:", walletA.get_balance())
    print("\nWalletA is Attempting to send funds (40) to WalletB...")
    block1.add_transaction(walletA.send_funds(walletB.public_key, 40),blockchain)
    blockchain.add_block(block1)
    print("\nWalletA's balance is:", walletA.get_balance())
    print("WalletB's balance is:", walletB.get_balance())

    block2 = Block(block1.hash)
    print("\nWalletA Attempting to send more funds (1000) than it has...")
    block2.add_transaction(walletA.send_funds(walletB.public_key, 1000),blockchain)
    blockchain.add_block(block2)
    print("\nWalletA's balance is:", walletA.get_balance())
    print("WalletB's balance is:", walletB.get_balance())

    block3 = Block(block2.hash)
    print("\nWalletB is Attempting to send funds (20) to WalletA...")
    block3.add_transaction(walletB.send_funds(walletA.public_key, 20, ),blockchain)
    blockchain.add_block(block3)
    print("\nWalletA's balance is:", walletA.get_balance())
    print("WalletB's balance is:", walletB.get_balance())

# validating the blockchain
    print("\nIs blockchain valid?", blockchain.is_chain_valid())
    print(blockchain.to_json())

if __name__ == "__main__":
    main()

