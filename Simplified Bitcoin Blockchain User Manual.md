# Simplified Bitcoin Blockchain User Manual

# Simplified Bitcoin Blockchain User Manual

## 1. Introduction

This document provides a guide for operating `blockchain_sim.py`, explaining the meaning of each command and the reasoning behind its design. This program is a simplified blockchain simulator that demonstrates fundamental blockchain mechanisms, including block creation, transaction addition, hashing operations, and Proof of Work (PoW) mining. This version supports Docker containerization for easy deployment and management.

## 2. Execution Environment

### 2.1 Required Packages

Ensure that Python is installed (Python 3.8 or later is recommended). If additional dependencies are required, install them using:

```
pip install -r requirements.txt

```

(If `requirements.txt` does not exist, `hashlib` and `time` are standard libraries and require no additional installation.)

### 2.2 Execution Methods

### Local Execution

Run the following command in the terminal:

```
python blockchain_sim.py

```

### Docker Execution

This project supports Docker containerization. Follow these steps to run it:

1. **Navigate to the project directory**:

```
cd blockchain_sim

```

1. **Build the Docker image**:

```
docker build -t blockchain-sim .

```

1. **Run the container**:

Basic execution (5 participants):

```
docker run blockchain-sim

```

Enable debug mode:

```
docker run blockchain-sim --debug

```

Specify the number of participants:

```
docker run blockchain-sim --parties 3

```

Use multiple parameters:

```
docker run blockchain-sim --debug --parties 3

```

## 3. Main Features and Command Descriptions

### 3.1 Blockchain Creation (`Blockchain` Class)

The core of the program is the `Blockchain` class, responsible for managing the blockchain, transactions, blocks, and mining mechanisms.

- **`__init__()`**
    - Initializes the blockchain and creates the Genesis Block.
    - The `previous_hash` of the Genesis Block is set to `0`, indicating the start of the chain.
    - **Reason**: The first block in a blockchain has no predecessor, so a special marker is needed.

### 3.2 Adding Transactions (`add_transaction` Method)

```python
blockchain.add_transaction(sender, receiver, amount)

```

- **Function**: Adds a transaction to the blockchain’s pending transaction pool.
- **Parameters**:
    - `sender`: Transaction sender.
    - `receiver`: Transaction recipient.
    - `amount`: Transaction amount.
- **Reason**: Transactions must first be added to the pool before they can be included in a block.

### 3.3 Mining (`mine_block` Method)

```python
blockchain.mine_block(miner_address)

```

- **Function**: Executes PoW mining and packages transactions into a new block.
- **Parameters**:
    - `miner_address`: The address of the miner who receives the block reward.
- **Reason**:
    - Mining is a core blockchain mechanism that ensures block validity through PoW.
    - The miner must compute a hash that meets difficulty requirements (e.g., a specified number of leading `0`s).
    - Miners receive rewards to incentivize blockchain maintenance.

### 3.4 Retrieving Blockchain Information (`get_chain` Method)

```python
blockchain.get_chain()

```

- **Function**: Returns the current blockchain.
- **Reason**: Users can view the complete blockchain history and verify transactions.

### 3.5 Validating the Blockchain (`is_chain_valid` Method)

```python
blockchain.is_chain_valid()

```

- **Function**: Checks blockchain integrity to ensure no blocks have been tampered with.
- **Reason**:
    - Ensures that each block’s hash matches the previous block’s hash.
    - Prevents malicious users from altering transaction data.

## 4. Docker Common Issues and Solutions

### Permission Issues

```
# Linux/Mac
sudo docker build -t blockchain-sim .
sudo docker run blockchain-sim

```

### Port Conflicts

```
docker run -p 8080:8080 blockchain-sim

```

### Viewing Logs

```
docker logs blockchain-sim

```

### Cleaning Up Environment

If you need to clean up the Docker environment:

```
# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove the image
docker rmi blockchain-sim

```

## 5. Expansion Suggestions

- **Implement P2P Networking**: Currently, the blockchain runs on a single machine. Use Flask or WebSocket for node communication.
- **Support Smart Contracts**: Enable more complex transaction logic.
- **Improve Consensus Mechanism**: Experiment with PoS (Proof of Stake) and other consensus mechanisms.

## 6. Conclusion

This document provides a user guide for `blockchain_sim.py`, explaining the purpose and design of each command. Through this simplified blockchain, you can learn core blockchain concepts and improve it for more advanced applications.