from transaction import Transaction,TransactionOutput, TransactionInput
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256


class Wallet :

    def __init__(self,blockchain):
        self.private_key = None
        self.public_key = None
        self.blockchain = blockchain
        self.generate_key_pair()
        self.UTXOs ={}


    def generate_key_pair(self):
        try :
            # using the ECC  lib to generate a  keypair of the public key and private key     
            key = ECC.generate(curve='P-192')
            self.private_key = key
            self.public_key = key.public_key()      
        except Exception as e: 
            raise RuntimeError(e)
    

  #returns balance and stores the UTXO's owned by this wallet in self.UTXOs
    

    def get_balance(self):
        return self.blockchain.get_balance(self.public_key)

    def get_UTXOs(self):
        return {utxo_id: utxo for utxo_id, utxo in self.blockchain.UTXOs.items() if utxo.is_mine(self.public_key)}

    def send_funds(self, recipient, value):
        if self.get_balance() < value:
            print("#Not Enough funds to send transaction. Transaction Discarded.")
            return None

        inputs = []
        total = 0
        my_UTXOs = self.get_UTXOs()

        for utxo_id, utxo in my_UTXOs.items():
            total += utxo.value
            inputs.append(TransactionInput(utxo_id))
            if total >= value:
                break

        if total < value:
            print("#Not enough UTXOs to cover the transaction. Transaction Discarded.")
            return None

        new_transaction = Transaction(self.public_key, recipient, value, inputs)
        new_transaction.generate_signature(self.private_key)

        change = total - value
        if change > 0:
            new_transaction.outputs.append(TransactionOutput(self.public_key, change, new_transaction.transaction_id))

        return new_transaction
       