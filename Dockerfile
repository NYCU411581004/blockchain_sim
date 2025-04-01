# 使用官方 Python 映像作為基礎
FROM python:3.12-slim

# 設置工作目錄
WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY blockchain_sim.py .

# 設置環境變數
ENV PYTHONUNBUFFERED=1

# 執行應用程式
ENTRYPOINT ["python", "blockchain_sim.py"] 