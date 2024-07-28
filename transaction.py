from string_util import string_util
from Crypto.PublicKey import ECC

class TransactionOutput:
    def __init__(self, recipient: ECC.EccKey, value: float, parent_transaction_id: str) -> None:
        self.recipient = recipient
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        self.id = self.calculate_id()

    def calculate_id(self):
        return string_util.apply_sha_256(
            string_util.get_string_from_key(self.recipient) +
            str(self.value) +
            self.parent_transaction_id
        )

    def is_mine(self, public_key: ECC.EccKey) -> bool:
        return public_key == self.recipient

class TransactionInput:
    def __init__(self, transaction_output_id: str) -> None:
        self.transaction_output_id = transaction_output_id
        self.UTXO = None

class Transaction:
    transaction_number = 0

    def __init__(self, sender: ECC.EccKey, recipient: ECC.EccKey, value: float, inputs: list) -> None:
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.inputs = inputs
        self.outputs = []
        self.transaction_id = self.calculate_hash()
        self.signature = None

    def calculate_hash(self):
        Transaction.transaction_number += 1
        data = (
            string_util.get_string_from_key(self.sender) +
            string_util.get_string_from_key(self.recipient) +
            str(self.value) +
            str(Transaction.transaction_number)
        )
        return string_util.apply_sha_256(data)

    def generate_signature(self, private_key: ECC.EccKey) -> None:
        data = (
            string_util.get_string_from_key(self.sender) +
            string_util.get_string_from_key(self.recipient) +
            str(self.value)
        )
        self.signature = string_util.apply_ECDSA_sig(private_key, data)

    def verify_signature(self) -> bool:
        data = (
            string_util.get_string_from_key(self.sender) +
            string_util.get_string_from_key(self.recipient) +
            str(self.value)
        )
        return string_util.verify_ECDSA_sig(self.sender, data, self.signature)

    def get_inputs_value(self) -> float:
        total = 0
        for input in self.inputs:
            if input.UTXO:
                total += input.UTXO.value
        return total

    def get_outputs_value(self) -> float:
        return sum(output.value for output in self.outputs)

    def generate_outputs(self) -> None:
        left_over = self.get_inputs_value() - self.value
        self.outputs.append(TransactionOutput(self.recipient, self.value, self.transaction_id))
        if left_over > 0:
            self.outputs.append(TransactionOutput(self.sender, left_over, self.transaction_id))

    def process_transaction(self, blockchain) -> bool:
        if not self.verify_signature():
            print("#Transaction Signature failed to verify")
            return False

        # gather transaction inputs and verify they are unspent
        for input in self.inputs:
            input.UTXO = blockchain.get_UTXO(input.transaction_output_id)
            if not input.UTXO:
                print(f"#Referenced input on Transaction({self.transaction_id}) is Missing")
                return False

        if self.get_inputs_value() < blockchain.minimum_transaction:
            print(f"#Transaction Inputs too small: {self.get_inputs_value()}")
            return False

        self.generate_outputs()

        # add outputs to blockchain's UTXO list
        for output in self.outputs:
            blockchain.UTXOs[output.id] = output

        # remove transaction inputs from UTXO list as spent
        for input in self.inputs:
            if input.UTXO:
                blockchain.UTXOs.pop(input.UTXO.id, None)

        return True