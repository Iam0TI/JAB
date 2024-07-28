from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC


class string_util:
    @staticmethod
    def get_string_from_key(key: ECC.EccKey) -> str:
        return key.export_key(format='DER').hex()

# a helper function to get create digital signature 
    @staticmethod
    def apply_ECDSA_sig(private_key: ECC.EccKey, data: str) -> bytes:
        data_hash = SHA256.new(data.encode('utf-8'))
        signer = DSS.new(private_key, 'fips-186-3')
        return signer.sign(data_hash)
    
 # a helper function to verify signature 
    @staticmethod
    def verify_ECDSA_sig(public_key: ECC.EccKey, data: str, signature: bytes) -> bool:
        data_hash = SHA256.new(data.encode('utf-8'))
        verifier = DSS.new(public_key, 'fips-186-3')
        try:
            verifier.verify(data_hash, signature)
            return True
        except ValueError:
            return False

    # Converts input string to bytes        
    # Creates a new SHA-256 hash object and update it with the input bytes
    @staticmethod
    def apply_sha_256(strinput: str) -> str:
        try:
            hash_str = SHA256.new(strinput.encode('utf-8')).hexdigest()
            return hash_str
        except Exception as e:
            raise RuntimeError(e)
        
    

