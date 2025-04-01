# 區塊鏈模擬器

這是一個使用 Python 實現的區塊鏈模擬器，可以在 Docker 環境中運行。

## 環境要求

- Docker Desktop（Windows/Mac/Linux）
- 確保 Docker 服務正在運行

## 專案檔案結構

```
blockchain_sim/
├── blockchain_sim.py    # 主程式
├── requirements.txt     # Python 依賴
├── Dockerfile          # Docker 配置文件
├── .dockerignore       # Docker 忽略文件
└── README.md           # 說明文件
```

## 執行步驟

1. **進入專案目錄**：
```bash
cd blockchain_sim
```

2. **建立 Docker 映像**：
```bash
docker build -t blockchain-sim .
```

3. **運行容器**：

基本運行（5個參與者）：
```bash
docker run blockchain-sim
```

啟用除錯模式：
```bash
docker run blockchain-sim --debug
```

指定參與者數量：
```bash
docker run blockchain-sim --parties 3
```

同時使用多個參數：
```bash
docker run blockchain-sim --debug --parties 3
```

## 常見問題解決

### 權限問題
```bash
# Linux/Mac
sudo docker build -t blockchain-sim .
sudo docker run blockchain-sim
```

### 端口衝突
```bash
docker run -p 8080:8080 blockchain-sim
```

### 查看日誌
```bash
docker logs blockchain-sim
```

## 清理環境

如果需要清理 Docker 環境：
```bash
# 停止所有容器
docker stop $(docker ps -a -q)

# 刪除所有容器
docker rm $(docker ps -a -q)

# 刪除映像
docker rmi blockchain-sim
```

## 注意事項

- 確保 Docker Desktop 已經啟動
- 確保有足夠的磁碟空間
- 確保網路連接正常（需要下載 Python 映像和依賴包）
- 第一次運行可能需要較長時間，因為需要下載基礎映像和安裝依賴

## 驗證安裝

```bash
# 檢查 Docker 是否正確安裝
docker --version

# 檢查映像是否成功建立
docker images | grep blockchain-sim
```

## 開發模式

如果需要修改程式碼並即時測試：
```bash
# 使用卷掛載運行
docker run -v $(pwd):/app blockchain-sim
```

## 參數說明

- `--debug`：啟用除錯模式，顯示詳細的日誌輸出
- `--parties N`：設置參與者數量，預設為 5

## 輸出說明

程式會輸出：
- 區塊鏈的創建過程
- 交易的生成和驗證
- 挖礦的進度
- 最終的區塊鏈狀態

## 故障排除

如果遇到問題，請檢查：
1. Docker 是否正確安裝
2. 網路連接是否正常
3. Docker 日誌是否有錯誤訊息
4. 所有必要檔案是否存在 
