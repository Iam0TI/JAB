import string_util
from Crypto.PublicKey import ECC



class Transaction :
    transaction_number = 0 
    def __init__(self, sender:ECC.EccKey , reciepient:ECC.EccKey, value:float, inputs:list ) -> None:
        self.sender = sender
        self.reciepent = reciepient
        self.value = value
        # inputs are references to previous transactions that prove the sender has funds to send.
        self.inputs = inputs 
        self.transaction_id = self.calculate_hash()
        self.signature = None
        self.outputs = []


    #This Calculates the transaction hash (which will be used as its Id)
    def calulate_hash (self):
        transaction_number +=1
     #o_hash =  self.sender + self.reciepient
        data = (
            string_util.get_string_from_key(self.sender) +
            string_util.get_string_from_key(self.recipient) +
            str(self.value) + str(Transaction.transaction_number)
        )
        return string_util.apply_sha_256(data)

