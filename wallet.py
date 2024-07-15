from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import hashlib




class Wallet :

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_key_pair()

    def generate_key_pair(self):
        try :
            # using the ECC  lib to generate a  keypair of the public key and private key 
            
            key = ECC.generate(curve='P-192')
            self.private_key = key
            self.public_key = key.public_key()
            
        except Exception as e: 
            raise RuntimeError(e)
        

        

       