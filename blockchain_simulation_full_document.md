# Blockchain Simulation - Comprehensive Documentation

## 📌 Design & Algorithm Description

**Design & Algorithm Description**

---

**1. Blockchain Structure**

The blockchain is a list of sequential blocks, each containing:
- `index`: Position in the chain.
- `previous_hash`: Hash of the previous block to ensure integrity.
- `transactions`: List of transactions in the block.
- `timestamp`: Unix time when the block was created.
- `nonce`: Integer used to compute proof-of-work.
- `hash`: The SHA-256 hash of the block's content.

The genesis block (index 0) is manually created with a previous hash of 64 zeros and no transactions.

---

**2. Transaction Format and Validation**

Each transaction includes:
- `sender`: Name of the sending party.
- `receiver`: Name of the receiving party.
- `value`: Positive integer value of the transaction.
- `timestamp`: Creation time.
- `signature`: Hex string of the digital signature.

**Validation Process:**
- Ensures non-negative, non-zero value.
- Rejects self-transactions.
- Verifies sender's balance.
- Uses RSA public key signature verification for authenticity.

---

**3. Mining and Block Creation Logic**

- Parties collect transactions until a minimum threshold (5) or timeout (60s) triggers mining.
- Mining involves computing a SHA-256 hash of the block data with a `nonce` until it starts with two zeros ("00").
- If successful within time limit, block is added to the blockchain after verification.

**Block Verification Includes:**
- Validating hash prefix.
- Matching previous hash with last block.
- Verifying each transaction.

---

**4. Consensus Mechanism**

This simulation adopts a centralized mining model based on lowest IP address value. There is no distributed consensus protocol like PoW or PoS across nodes.

The miner is deterministically chosen, and no fork resolution is implemented.

---

**Documentation**

---

**1. Instructions to Run the Simulation**

**Requirements:**
- Python 3.9+
- `cryptography` library

**Run Command:**
```bash
python blockchain_sim.py
```

To enable debug logs:
```bash
python blockchain_sim.py --debug
```

---

**2. Verifying the Blockchain**

At random intervals (10% probability per iteration) and at the end of simulation, the simulator verifies:
- Block index ordering
- Previous hash linkage
- Valid transactions and correct mining difficulty
- Integrity of genesis block

Final result is printed and logged.

---

**3. Docker Execution (Optional)**

To run in Docker:

**Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY blockchain_sim.py .
RUN pip install cryptography
CMD ["python", "blockchain_sim.py"]
```

**Build and Run:**
```bash
docker build -t blockchain-sim .
docker run --rm blockchain-sim
```

---

## 📘 Documentation

### 📄 操作手冊
# 簡化版比特幣區塊鏈操作手冊

# 簡化版比特幣區塊鏈操作手冊

## 1. 簡介

本文件提供對 `blockchain_sim.py` 的操作指南，並解釋各指令的含義及其設計背後的原因。本程式為一個簡化的區塊鏈模擬器，展示了基本的區塊鏈運作機制，包括區塊的建立、交易的加入、哈希運算、PoW 挖礦機制等。本版本支援 Docker 容器化運行，方便快速部署與管理。

## 2. 執行環境

### 2.1 必要套件

請確保您的環境已安裝 Python（建議使用 Python 3.8 以上版本）。如果程式依賴額外的 Python 套件，請先執行以下命令來安裝：

```
pip install -r requirements.txt

```

(如果 `requirements.txt` 不存在，請直接安裝 `hashlib` 和 `time`，這些是標準庫，不需要額外安裝。)

### 2.2 執行方式

### 本地運行

在終端機中輸入以下指令執行程式：

```
python blockchain_sim.py

```

### Docker 運行

本專案已支援 Docker 容器化，可使用以下步驟執行。

1. **進入專案目錄**：

```
cd blockchain_sim

```

1. **建立 Docker 映像**：

```
docker build -t blockchain-sim .

```

1. **運行容器**：

基本運行（5個參與者）：

```
docker run blockchain-sim

```

啟用除錯模式：

```
docker run blockchain-sim --debug

```

指定參與者數量：

```
docker run blockchain-sim --parties 3

```

同時使用多個參數：

```
docker run blockchain-sim --debug --parties 3

```

## 3. 主要功能與指令說明

### 3.1 建立區塊鏈（Blockchain 類別）

程式的核心是 `Blockchain` 類別，該類別負責管理整個區塊鏈，包括交易、區塊以及挖礦機制。

- **`__init__()`**
    - 初始化區塊鏈，並創建創世區塊（Genesis Block）。
    - 創世區塊的 `previous_hash` 設為 `0`，代表它是鏈的起點。
    - 原因：區塊鏈的第一個區塊沒有前一個區塊，因此需要一個特殊的標記。

### 3.2 新增交易（`add_transaction` 方法）

```python
blockchain.add_transaction(sender, receiver, amount)

```

- **功能**：將交易加入到區塊鏈的待處理交易池中。
- **參數**：
    - `sender`：交易發送者。
    - `receiver`：交易接收者。
    - `amount`：交易金額。
- **原因**：區塊鏈的交易需要先被加入交易池，稍後才能被打包進區塊。

### 3.3 挖礦（`mine_block` 方法）

```python
blockchain.mine_block(miner_address)

```

- **功能**：執行 PoW 挖礦機制，並將交易打包進新的區塊。
- **參數**：
    - `miner_address`：礦工的地址，用於獲取區塊獎勵。
- **原因**：
    - 挖礦是區塊鏈的核心機制之一，透過 PoW（Proof of Work）確保區塊的有效性。
    - 礦工需要計算哈希值，使其符合難度要求（如前導 `0` 的數量）。
    - 獎勵礦工，確保系統有動機來維護區塊鏈。

### 3.4 取得區塊鏈資訊（`get_chain` 方法）

```python
blockchain.get_chain()

```

- **功能**：回傳目前的區塊鏈。
- **原因**：用戶可以查看區塊鏈的完整歷史，驗證交易。

### 3.5 驗證區塊鏈（`is_chain_valid` 方法）

```python
blockchain.is_chain_valid()

```

- **功能**：檢查區塊鏈的完整性，確保沒有區塊被篡改。
- **原因**：
    - 確保區塊的哈希值與前一個區塊的哈希值匹配。
    - 防止惡意用戶竄改交易數據。

## 4. Docker 常見問題與解決方案

### 權限問題

```
# Linux/Mac
sudo docker build -t blockchain-sim .
sudo docker run blockchain-sim

```

### 端口衝突

```
docker run -p 8080:8080 blockchain-sim

```

### 查看日誌

```
docker logs blockchain-sim

```

### 清理環境

如果需要清理 Docker 環境：

```
# 停止所有容器
docker stop $(docker ps -a -q)

# 刪除所有容器
docker rm $(docker ps -a -q)

# 刪除映像
docker rmi blockchain-sim

```

## 5. 擴充建議

- **引入 P2P 網路**：目前區塊鏈僅限於單機運行，可透過 Flask 或 WebSocket 建立節點間的通訊。
- **智能合約支持**：允許更複雜的交易邏輯。
- **共識機制改進**：可以嘗試 PoS（Proof of Stake）等不同共識機制。

## 6. 結論

這份文件提供了 `blockchain_sim.py` 的操作指南，並解釋了各指令的目的與設計原因。透過這個簡化版本的區塊鏈，你可以學習到區塊鏈的核心概念，並進一步改進以符合更高階的應用需求。

---

## 📖 原理說明
# 區塊鏈模擬器說明

## 什麼是區塊鏈？

想像一個特殊的記帳本，這個記帳本有以下特點：
1. 每個人都有一份完整的副本
2. 新的交易會被打包成一個「區塊」
3. 每個區塊都與前一個區塊相連，形成一條「鏈」
4. 一旦記錄就不能被修改
5. 所有人都可以驗證交易的真實性

## 這個模擬器在做什麼？

這個程式模擬了一個簡單的區塊鏈系統，包含以下角色：
- **參與者**：可以進行交易的用戶
- **交易**：參與者之間的資金轉移
- **礦工**：負責將交易打包成區塊的人
- **區塊**：包含多筆交易的資料包

## 主要功能說明

### 1. 參與者系統
- 每個參與者都有：
  - 獨特的 IP 地址（就像網路上的門牌號碼）
  - 1000 元的初始資金
  - 自己的密鑰（用於簽名交易）

### 2. 交易系統
- 參與者可以：
  - 發送交易給其他參與者
  - 每次交易金額必須是正整數
  - 不能發送超過自己餘額的金額
  - 每次交易後需要等待 1-16 秒才能進行下一筆交易

### 3. 挖礦系統
- 當交易池中有 5 筆以上的交易，或等待超過 60 秒時，就會觸發挖礦
- 系統會選擇 IP 地址最小的參與者作為礦工
- 礦工需要解決一個數學難題（找到特定的雜湊值）
- 成功後，新的區塊會被添加到區塊鏈中

### 4. 驗證系統
- 每筆交易都需要：
  - 發送者的簽名
  - 足夠的餘額
  - 接收者的確認
- 每個區塊都需要：
  - 正確的雜湊值
  - 與前一個區塊的正確連結
  - 所有交易的驗證

## 技術細節解釋

### 1. 檔案結構
```
blockchain_sim/
├── blockchain_sim.py    # 主程式
├── requirements.txt     # 需要的程式套件清單
├── Dockerfile          # Docker 環境設定
├── .dockerignore       # Docker 忽略的檔案
└── README.md           # 使用說明
```

### 2. 重要指令解釋
```bash
# 建立 Docker 映像（就像建立一個虛擬的電腦環境）
docker build -t blockchain-sim .

# 運行程式（啟動虛擬環境並執行程式）
docker run blockchain-sim

# 啟用除錯模式（顯示更多執行細節）
docker run blockchain-sim --debug

# 設定參與者數量
docker run blockchain-sim --parties 3
```

### 3. 安全機制
- 使用 RSA 加密進行交易簽名
- 每個區塊都有唯一的雜湊值
- 區塊之間通過雜湊值相連，確保資料完整性
- 交易需要多重驗證才能被接受

## 實際運作流程

1. **初始化**：
   - 創建指定數量的參與者
   - 每個參與者獲得初始資金
   - 建立創世區塊

2. **交易階段**：
   - 隨機選擇參與者進行交易
   - 驗證交易的有效性
   - 將有效交易加入交易池

3. **挖礦階段**：
   - 選擇礦工
   - 打包交易成新區塊
   - 進行挖礦運算
   - 驗證並添加新區塊

4. **驗證階段**：
   - 定期檢查整個區塊鏈的有效性
   - 確保所有交易和區塊都是正確的

## 使用情境

這個模擬器可以用於：
- 學習區塊鏈的基本概念
- 理解加密貨幣的運作原理
- 研究區塊鏈的安全性機制
- 測試不同的交易模式

## 注意事項

1. 這是一個教學用的模擬器，不適合用於實際的加密貨幣交易
2. 模擬器中的難度設定較低，實際的區塊鏈系統會更複雜
3. 需要足夠的電腦資源才能運行
4. 第一次運行可能需要較長時間下載必要的程式 

---

## 📦 Python Requirements

```txt
cryptography>=42.0.0
ipaddress>=1.0.23
```
