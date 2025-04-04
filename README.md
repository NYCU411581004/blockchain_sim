# README

## **一、簡介**

本文件旨在提供一個詳盡的操作指南，用於理解和運行 `blockchain_sim.py`，這是一個使用 Python 實現的簡化區塊鏈模擬器。本模擬器展示了區塊鏈的核心運作機制，包括**區塊的建立**、**交易的加入**、**雜湊運算**以及**工作量證明（Proof of Work, PoW）挖礦**等。本版本支援 **Docker 容器化運行**，方便部署和管理。透過這個模擬器，使用者可以學習區塊鏈的基本概念，並理解加密貨幣的運作原理。

## **二、區塊鏈基礎概念**

### 區塊鏈可以想像成一個特殊的記帳本，具備以下特點：

- **去中心化**：每個人都擁有一份完整的副本。
- **區塊鏈接**：新的交易會被打包成「區塊」，每個區塊都與前一個區塊相連，形成一條「鏈」。
- **不可篡改**：一旦記錄到區塊鏈上的資訊就難以修改。
- **公開透明**：所有人都可以驗證交易的真實性。

## **三、模擬器功能與設計**

### 本模擬器模擬了一個簡單的區塊鏈系統，包含以下核心元素:

- **參與者**：可以進行交易的用戶，每個參與者擁有一個獨特的 IP 地址、初始資金以及自己的密鑰（用於簽名交易）。
- **交易**：參與者之間發生的資金轉移，交易金額必須為正整數，且不能超過發送者的餘額。每筆交易都包含發送者、接收者、金額和時間戳記，並使用 RSA 私鑰進行數位簽章。交易在被打包到區塊前，會先儲存在交易池中。交易需要經過驗證，包括檢查金額、發送者餘額和簽章。
- **區塊**：包含多筆已驗證交易的資料包。每個區塊包含索引、前一個區塊的雜湊值 (`previous_hash`)、交易清單 (`transactions`)、時間戳記 (`timestamp`)、用於工作量證明的變數 (`nonce`) 以及自身的雜湊值 (`hash`)。**創世區塊**是區塊鏈中的第一個區塊，其 `previous_hash` 設定為 0 或 64 個零。
- **礦工**：負責將交易池中的交易打包成新的區塊，並透過解決一個數學難題（找到符合難度要求的雜湊值，例如前綴為兩個零 `"00"`）來進行挖礦。挖礦過程是透過調整區塊中的 `nonce` 值，計算區塊的 SHA-256 雜湊值，直到滿足難度要求。成功挖礦的礦工可能會獲得獎勵（雖然在目前的簡化版本中可能未明確提及獎勵機制）。本模擬器會選擇 IP 位址數值最小的參與者作為礦工。
- **區塊鏈**：由多個區塊依時間順序鏈式連接而成。每個新區塊都包含前一個區塊的雜湊值，確保鏈的連續性和資料的不可篡改性。

## **四、執行模擬器**

本模擬器支援兩種執行方式：**本地執行**和使用 **Docker 執行**。

### **4.1 環境要求**

- **Python 環境**：建議使用 Python 3.8 或以上版本。
- **Docker**：如果選擇 Docker 執行，需要安裝 **Docker Desktop**（適用於 Windows/Mac/Linux）並確保 Docker 服務正在運行。
- **依賴套件**：如果程式依賴額外的 Python 套件，可以使用 `pip install -r requirements.txt` 命令進行安裝。如果 `requirements.txt` 不存在，`hashlib` 和 `time` 通常是標準庫，不需要額外安裝。
- **網路連接**：第一次運行可能需要網路連接以下載基礎 Docker 映像和安裝依賴包。
- **磁碟空間**：確保有足夠的磁碟空間來儲存 Docker 映像和容器。

### **4.2 執行步驟**

**方法一：本地執行**

1. **進入專案目錄**：在終端機中導航至包含 `blockchain_sim.py` 檔案的目錄。
2. **執行指令**：在終端機中輸入 `python blockchain_sim.py [參數]` 來運行程式。

**方法二：使用 Docker 執行**

1. **進入專案目錄**：在終端機中導航至包含 `Dockerfile` 和 `blockchain_sim.py` 檔案的目錄。
2. **建立 Docker 映像**：執行命令 `docker build -t blockchain-simulator .` 來建立 Docker 映像。 (`blockchain-simulator` 可以替換為您想要的映像名稱)。
3. **運行容器**：使用 `docker run [選項] blockchain-simulator [參數]` 命令來運行 Docker 容器。

### **4.3 執行參數**

可以在執行命令時添加以下參數來配置模擬器：

- `-debug`：啟用除錯模式，顯示更詳細的日誌輸出。
- `-parties N`：設置參與者的數量，預設為 5。可以將 `N` 替換為所需的參與者數量。

**範例執行命令**:

- **基本運行（5 個參與者）**：
    - 本地執行：`python blockchain_sim.py`
    - Docker 執行：`docker run blockchain-simulator`
- **啟用除錯模式**：
    - 本地執行：`python blockchain_sim.py --debug`
    - Docker 執行：`docker run blockchain-simulator --debug`
- **指定參與者數量（例如 10 個）**：
    - 本地執行：`python blockchain_sim.py --parties 10`
    - Docker 執行：`docker run blockchain-simulator --parties 10`
- **同時使用多個參數**：
    - 本地執行：`python blockchain_sim.py --debug --parties 3`
    - Docker 執行：`docker run blockchain-simulator --debug --parties 3`

## **五、模擬器輸出說明**

程式運行時會輸出以下資訊：

- 區塊鏈的創建過程（包括創世區塊的建立）。
- 交易的生成和驗證過程。
- 挖礦的進度。
- 最終的區塊鏈狀態。

## **六、區塊鏈驗證**

模擬器會定期（約每十次操作隨機驗證一次）以及在模擬結束時自動驗證整個區塊鏈的有效性。驗證內容包括:

- 創世區塊的正確性。
- 每個區塊的索引是否與其在鏈中的位置一致。
- 每個區塊的 `previous_hash` 是否與前一個區塊的 `hash` 值相符，確保鏈的連續性。
- 區塊中包含的每筆交易是否都經過有效的簽章驗證且合法（例如，發送者餘額是否足夠）。
- 每個區塊的雜湊值是否符合預設的難度要求（例如，前綴是否包含指定數量的零）。

## **七、Docker 相關常見問題與解決方案**

- **權限問題**：在 Linux 或 macOS 上運行 Docker 命令時，如果遇到權限錯誤，可以嘗試使用 `sudo` 命令來執行。
- **端口衝突**：如果模擬器嘗試使用的端口已被其他程式佔用，可能會導致錯誤。請檢查是否有其他服務正在使用相同的端口，並考慮更改模擬器使用的端口（如果程式有相關配置）。
- **查看日誌**：可以使用 `docker logs <容器ID或名稱>` 命令來查看 Docker 容器的輸出日誌，這對於排查問題非常有幫助。可以使用 `docker ps -a` 命令列出所有容器，包括正在運行和已停止的容器，以找到目標容器的 ID 或名稱。
- **映像無法建立**：請確認 `Dockerfile` 存在於專案目錄中，並且其語法是正確的。
- **無法運行**：檢查您的系統是否已正確安裝 Docker，並確認 Docker 服務正在運行。
- **清理環境**：如果需要清理 Docker 環境，可以停止並移除正在運行的容器 (`docker stop <容器ID或名稱>` 和 `docker rm <容器ID或名稱>`)，並移除不再需要的映像 (`docker rmi <映像ID或名稱>`). 可以使用 `docker system prune` 命令清理不再被 Docker 使用的資源。

## **八、注意事項**

1. 這是一個測試用的模擬器，不適合用於實際的加密貨幣交易。
2. 模擬器中的難度設定較低，實際的區塊鏈系統會更複雜。
3. 第一次運行可能需要較長時間，因為需要下載基礎映像和安裝依賴。
4. 確保 Docker Desktop 已經啟動（如果使用 Docker 運行）。
5. 確保網路連接正常（第一次運行需要下載 Python 映像和依賴包）。
6. 確保所有必要的檔案（例如 `blockchain_sim.py`, `Dockerfile`, 可能的 `requirements.txt`）都存在於正確的目錄中。

## **九、擴充建議**

本模擬器可以進一步擴展，以包含更複雜的功能：

- **引入 P2P 網路**：目前模擬器僅在單機上運行，可以透過 Flask 或 WebSocket 等技術建立節點之間的通訊，模擬分散式網路。
- **支援智能合約**：允許在區塊鏈上執行更複雜的交易邏輯和應用程式。
- **改進共識機制**：實驗不同的共識演算法，例如權益證明（Proof of Stake, PoS）或其他更複雜的共識機制，以模擬更真實的區塊鏈環境。
- **更完善的交易系統**：例如，支援交易費用、更複雜的交易類型等。
- **圖形化介面**：開發一個使用者友好的圖形化介面，方便操作和觀察模擬器的運行情況。

## **十、總結**

本區塊鏈模擬器提供了一個簡化但完整的學習環境，透過 Python 和 Docker 容器技術，實現了交易建立、區塊打包、挖礦驗證和鏈接驗證等核心功能。其設計目的是為了幫助使用者理解區塊鏈的基本概念、交易簽章與驗證流程、區塊鏈的不可篡改性以及挖礦與共識機制。透過本文件提供的操作指引，使用者可以輕鬆地運行和調整模擬器的參數，觀察其行為變化，從而更深入地理解區塊鏈技術。
