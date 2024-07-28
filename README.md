# JAB (Just Another Blockchain )


# Basic Proof-of-Work Blockchain Implementation

This project is a basic implementation of a Proof-of-Work (PoW) blockchain in Python. The implementation is inspired by the tutorial [Creating Your First Blockchain with Java Part 2 - Transactions](https://medium.com/programmers-blockchain/creating-your-first-blockchain-with-java-part-2-transactions-2cdac335e0ce).

## What I learnt 
- The use of Merkle root
- The true meaning of blockchain being a legder
- UTXO
- How mining really works and the role of nonce
- Digital signature creatation and verification 
## Features

- Basic blockchain structure with blocks and transactions.
- Proof-of-Work algorithm to mine blocks.
- Digital signatures for transaction security.
- Adjustable difficulty for mining.
- Merkle root for transaction validtion
- Basic wallet implementation
## Dependencies

This project requires the following libraries:

- `json`
- `datetime`
- `pycryptodome` (for cryptographic functions)

You can install `pycryptodome` using pip:

```bash
pip install pycryptodome
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/JUSTFAVOUR/JAB.git
cd JAB
python test.py 
```

## Adjusting Mining Difficulty

You can adjust the mining difficulty by changing the difficulty variable in the blockchain.py file. This variable controls the amount of computational power and time required to mine a block.

```python

# blockchain.py

# Adjust this variable to increase or decrease mining difficulty
difficulty = 4
```
**NOTE**: you can write your test to interact with the code 

