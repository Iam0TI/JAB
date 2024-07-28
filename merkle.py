
from transaction import Transaction
from string_util import string_util

def get_merkle_root (transactions:Transaction) -> str :
        count : int = len(transactions)
        previous_tree_layer : list = []
        
        for transaction in transactions :
            previous_tree_layer.append(transaction.transaction_id)
        
        tree_layer = previous_tree_layer
        while (count > 1):
            tree_layer = []
            for i in range(1, len(previous_tree_layer)):
                tree_layer.append(string_util.apply_sha256(previous_tree_layer[i - 1] + previous_tree_layer[i]))
       
            count = len(tree_layer)

            previous_tree_layer = tree_layer
        merkle_root = tree_layer[0] if len(tree_layer) == 1 else ""

        return merkle_root



# import hashlib

# def get_merkle_root(transaction_ids):
#     if not transaction_ids:
#         return ''
#     while len(transaction_ids) > 1:
#         if len(transaction_ids) % 2 != 0:
#             transaction_ids.append(transaction_ids[-1])
#         new_level = []
#         for i in range(0, len(transaction_ids), 2):
#             new_level.append(hashlib.sha256((transaction_ids[i] + transaction_ids[i + 1]).encode()).hexdigest())
#         transaction_ids = new_level
#     return transaction_ids[0]

              
