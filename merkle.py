
from transaction import Transaction
from string_util import string_util

def get_merkle_root (transactions:Transaction) -> str :
        count : int = len(transactions)
        previous_tree_layer : list = []
        
        for transaction in transactions :
            previous_tree_layer.append(transactions.transaction_id)
        
        tree_layer = previous_tree_layer
        while (count > 1):
            tree_layer = []
            for i in range(1, len(previous_tree_layer)):
                tree_layer.append(string_util.apply_sha256(previous_tree_layer[i - 1] + previous_tree_layer[i]))
       
            count = len(tree_layer)

            previous_tree_layer = tree_layer
        merle_root = tree_layer[0] if len(tree_layer) == 1 else ""

        return merle_root
              
