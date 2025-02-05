# **README: Incentivizing Scientific Research Using a Reputation Scaled Proof of Stake Blockchain**

## **1. Overview**
This repository contains the implementation for my **Master’s Thesis** at **Hochschule Offenburg**, titled:
**"Incentivizing Scientific Research Using a Reputation Scaled Proof of Stake Blockchain."**

The system introduces a **Reputation Scaled Proof of Stake (RS-PoS)** consensus model designed to **incentivize scientific discussions and rational decision-making** on a decentralized platform. Unlike traditional **Proof of Stake (PoS)**, this model **incorporates reputation scores** into the staking mechanism, ensuring that validators are **not just financially strong but also knowledgeable contributors**.

---

## **2. Features**
- **Custom Proof of Stake Implementation** (RS-PoS) with a **reputation score multiplier**.
- **Smart Contracts for decentralized voting and consensus**.
- **Incentive model rewarding rational discourse and participation**.
- **Expert council for scientific validation**.
- **Fully functional blockchain implementation** in **Python**.

---

## **3. Repository Structure**
```
📂 Thesis-Final
 ├── AccountModel.py            # Manages user accounts and reputation system
 ├── Block.py                   # Defines the structure of a blockchain block
 ├── Blockchain.py               # Core blockchain functionality
 ├── BlockchainUtils.py          # Utility functions for the blockchain
 ├── Interaction.py - Interaction6.py  # Interaction modules for user engagement
 ├── Main.py                     # Entry point for executing the blockchain system
 ├── Message.py                   # Defines messages for blockchain communication
 ├── Node.py                      # Represents a blockchain node
 ├── NodeAPI.py                   # API for peer-to-peer communication
 ├── PeerDiscoveryHandler.py       # Manages peer discovery in the network
 ├── ProofOfStake.py               # Implements the Reputation Scaled PoS mechanism
 ├── SampleUseCase.py              # Example use case demonstrating platform behavior
 ├── SocketCommunication.py        # Handles network communication
 ├── SocketConnector.py            # Manages socket connections between nodes
 ├── Transaction.py                # Defines transaction structure
 ├── TransactionPool.py            # Pool for unprocessed transactions
 ├── Wallet.py                     # User wallet implementation
 ├── keys/                         # Folder for cryptographic keys
 ├── __pycache__/                  # Cached Python files
```

---

## **4. Class Descriptions**

### **🔹 AccountModel.py**
- Maintains user **balances, reputation weights, and participation history**.
- Stores **hashes of previous account states** to ensure transparency.

### **🔹 Block.py**
- Defines a **block** in the blockchain.
- Includes **transactions, timestamp, last block hash, and cryptographic signature**.

### **🔹 Blockchain.py**
- Handles **block validation, chain consistency, and consensus enforcement**.
- Implements **longest valid chain rule**.

### **🔹 ProofOfStake.py**
- **Implements the RS-PoS consensus mechanism**.
- Validators are selected based on **staked currency and reputation score**.
- Uses **normalized effective stake probability** to ensure fair selection.

### **🔹 Transaction.py**
- Implements different **types of transactions**:
  - **Stake transactions** for validators.
  - **Voting transactions** for consensus.
  - **Reward distribution transactions**.

### **🔹 Wallet.py**
- Handles **cryptographic key generation** and **signing transactions**.
- Implements **public-private key encryption** for identity management.

### **🔹 SampleUseCase.py**
- **Demonstrates** how users interact with the system.
- Includes:
  - **Genesis wallet creation**
  - **Delegates buying into an issue**
  - **Voting and council selection**
  - **Final consensus and rewards distribution**

---

## **5. Installation Guide**

### **Prerequisites**
- **Python 3.8+**
- **pip** installed

### **Setup Instructions**

1. **Clone the Repository**
```bash
git clone https://github.com/charan-coding/Thesis-Final.git
cd Thesis-Final
```

2. **Create a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Blockchain**
```bash
python Main.py
```

---

## **6. How the Code Works**

1. **Users create a wallet** (public-private key pair) and **stake tokens** to participate.
2. **Validators are selected** based on their **staked amount and reputation**.
3. **Delegates propose issues** by submitting transactions to the network.
4. **Voters stake tokens** to participate in **discussions and final voting**.
5. **A weighted voting system** (balancing majority opinion with expert knowledge) determines consensus.
6. **Winning delegates and voters are rewarded**, while misaligned opinions receive penalties.
7. **The process repeats**, ensuring a decentralized, reputation-driven system.

---

## **7. Future Improvements**
- **Smart Contract Integration** for **automated issue resolution**.
- **Enhanced Privacy Features** using **Zero-Knowledge Proofs (ZKPs)**.
- **Deployment of a prototype** on **Hyperledger Fabric or Ethereum**.

---

## **8. License**
This project is licensed under the **MIT License**.

---

## **9. Acknowledgments**
- **Prof. Dr. rer. nat Erik Zenner** – Supervisor and guide throughout this research.
- **Prof. Dr. phil. M.Sc Andreas Schaad** – Advisor on system modeling and research applications.
- **All contributors and peers** who provided invaluable insights.

---

This **README** provides a **structured and comprehensive** guide to your **Master's Thesis implementation**. Let me know if you'd like **any modifications or additional details!** 🚀

