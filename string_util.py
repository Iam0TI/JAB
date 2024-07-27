from hashlib import sha256
from Crypto.PublicKey import ECC
import base64

class string_util:
    
    def apply_sha_256( self, strinput: str) -> str:
        try:
            hash :str = sha256(strinput.encode('utf-8')).hexdigest()
            return hash 
        except Exception as e: 
            raise RuntimeError(e)
        
    def get_string_from_key(key: ECC.EccKey) -> str:
        return base64.b64encode(key.export_key(format='DER')).decode('utf-8')
