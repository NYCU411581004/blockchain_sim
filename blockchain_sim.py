import sys
import logging
from datetime import datetime
import traceback

# 設置日誌
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('blockchain.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

print("開始導入模組...")
sys.stdout.flush()
try:
    import hashlib
    print("已導入 hashlib")
    import json
    print("已導入 json")
    import random
    print("已導入 random")
    import time
    print("已導入 time")
    import argparse
    print("已導入 argparse")
    import ipaddress
    print("已導入 ipaddress")
    from typing import List, Dict, Optional, Tuple
    print("已導入 typing")
    from cryptography.hazmat.primitives import hashes
    print("已導入 cryptography.hazmat.primitives.hashes")
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    print("已導入 cryptography.hazmat.primitives.asymmetric")
    from cryptography.hazmat.primitives import serialization
    print("已導入 cryptography.hazmat.primitives.serialization")
except ImportError as e:
    logger.error(f"導入錯誤：{str(e)}")
    raise
except Exception as e:
    logger.error(f"未預期的錯誤：{str(e)}")
    raise

logger.info("所有模組導入成功")

class Transaction:
    def __init__(self, sender: str, receiver: str, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("交易金額必須為正整數")
        
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.timestamp = time.time()
        self.signature = None
        logger.debug(f"創建新交易：{sender} -> {receiver}，金額：{value}")

    def sign(self, private_key) -> bool:
        try:
            transaction_data = f"{self.sender}{self.receiver}{self.value}{self.timestamp}".encode()
            signature = private_key.sign(
                transaction_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.signature = signature.hex()
            logger.debug(f"交易簽名成功：{self.signature[:16]}...")
            return True
        except Exception as e:
            logger.error(f"交易簽名失敗：{str(e)}")
            return False

    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "value": self.value,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Transaction], timestamp: int):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = None
        self.mining_start_time = None
        logger.debug(f"創建新區塊 {index}，包含 {len(transactions)} 筆交易")

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, max_time: int = 60) -> Tuple[bool, int]:
        self.mining_start_time = time.time()
        attempts = 0
        
        while True:
            if time.time() - self.mining_start_time > max_time:
                logger.warning(f"區塊 {self.index} 挖礦超時")
                return False, attempts
                
            self.hash = self.calculate_hash()
            if self.hash.startswith("0" * 2):
                mining_time = time.time() - self.mining_start_time
                logger.info(f"區塊 {self.index} 挖礦成功，耗時：{mining_time:.2f}秒，嘗試次數：{attempts}")
                return True, attempts
                
            self.nonce += 1
            attempts += 1
            
            if attempts % 1000 == 0:  # 每1000次嘗試記錄一次日誌
                logger.debug(f"區塊 {self.index} 挖礦中，已嘗試 {attempts} 次")

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Party:
    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.transaction_pool: List[Transaction] = []
        self.public_keys = {}  # 存儲所有參與者的公鑰
        self.ip = str(ipaddress.IPv4Address(random.randint(0, 2**32-1)))  # 生成隨機 IP
        self.balance = 1000  # 初始餘額
        self.last_transaction_time = 0  # 記錄最後交易時間
        self.debug = debug  # 添加 debug 屬性
        logger.info(f"創建新參與者：{name}，IP：{self.ip}")

    def add_public_key(self, party_name: str, public_key):
        """添加其他參與者的公鑰"""
        self.public_keys[party_name] = public_key
        logger.debug(f"添加參與者 {party_name} 的公鑰")

    def get_public_key(self, party_name: str):
        """獲取指定參與者的公鑰"""
        if party_name == self.name:
            return self.public_key
        return self.public_keys.get(party_name)

    def create_transaction(self, receiver: str, value: int) -> Optional[Transaction]:
        try:
            # 檢查交易冷卻時間
            current_time = time.time()
            if current_time - self.last_transaction_time < random.uniform(1, 16):
                logger.debug(f"參與者 {self.name} 的交易冷卻時間未到")
                return None

            if not isinstance(value, int) or value <= 0:
                logger.warning(f"無效的交易金額：{value}")
                return None
                
            if receiver == self.name:
                logger.warning("發送者和接收者不能相同")
                return None

            # 檢查餘額是否足夠
            if self.balance < value:
                logger.warning(f"參與者 {self.name} 餘額不足：{self.balance} < {value}")
                return None
                
            transaction = Transaction(self.name, receiver, value)
            if transaction.sign(self.private_key):
                self.last_transaction_time = current_time
                self.balance -= value
                if self.debug:
                    logger.debug(f"參與者 {self.name} 創建新交易：接收者={receiver}，金額={value}，剩餘餘額={self.balance}")
                else:
                    logger.info(f"參與者 {self.name} 創建新交易")
                return transaction
            return None
        except Exception as e:
            logger.error(f"創建交易失敗：{str(e)}")
            return None

    def verify_transaction(self, transaction: Transaction) -> bool:
        try:
            if not transaction.sender or not transaction.receiver:
                logger.warning("交易缺少發送者或接收者")
                return False
                
            if transaction.sender == transaction.receiver:
                logger.warning("交易發送者和接收者相同")
                return False
                
            if not transaction.signature:
                logger.warning("交易缺少簽名")
                return False

            # 檢查發送者餘額
            if transaction.sender == self.name and self.balance < transaction.value:
                logger.warning(f"交易驗證失敗：發送者餘額不足")
                return False
                
            transaction_data = f"{transaction.sender}{transaction.receiver}{transaction.value}{transaction.timestamp}".encode()
            
            try:
                public_key = self.get_public_key(transaction.sender)
                public_key.verify(
                    bytes.fromhex(transaction.signature),
                    transaction_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                if self.debug:
                    logger.debug(f"交易驗證成功：{transaction.sender} -> {transaction.receiver}")
                return True
            except Exception as e:
                logger.warning(f"交易簽名驗證失敗：{str(e)}")
                return False
                
        except Exception as e:
            logger.warning(f"交易驗證失敗：{str(e)}")
            return False

class BlockchainSimulator:
    def __init__(self, num_parties: int = 5, debug: bool = False):
        if debug:
            logger.setLevel(logging.DEBUG)
            
        self.debug = debug
        self.num_parties = num_parties
        self.parties = [Party(f"Party_{i}", debug) for i in range(num_parties)]
        
        # 交換所有參與者的公鑰
        for party in self.parties:
            for other_party in self.parties:
                if other_party != party:
                    party.add_public_key(other_party.name, other_party.public_key)
        
        self.transaction_pool = []
        self.blockchain = []
        self.last_block_time = time.time()
        self.mining_timeout = 60
        self.min_transactions = 5
        self.max_transactions_per_block = 20
        self.max_blocks = 10
        self.total_transactions = 0
        self.total_blocks = 0
        
        logger.info(f"初始化區塊鏈，參與者數量：{num_parties}")
        
        # 創建創世區塊
        genesis_block = Block(0, "0" * 64, [], int(time.time()))
        success, attempts = genesis_block.mine()
        if success:
            self.blockchain.append(genesis_block)
            self.total_blocks += 1
            logger.info(f"創建創世區塊成功：{genesis_block.hash[:16]}...")
        else:
            raise RuntimeError("創建創世區塊失敗")

    def should_mine_block(self) -> bool:
        current_time = time.time()
        time_elapsed = current_time - self.last_block_time
        
        should_mine = (len(self.transaction_pool) >= self.min_transactions or 
                      time_elapsed >= self.mining_timeout)
        
        if should_mine:
            reason = "交易池已滿" if len(self.transaction_pool) >= self.min_transactions else "時間已到"
            logger.debug(f"觸發挖礦條件：{reason}")
            
        return should_mine

    def verify_block(self, block: Block) -> bool:
        try:
            # 驗證區塊雜湊值
            if not block.hash or not block.hash.startswith("0" * 2):
                logger.warning(f"區塊 {block.index} 雜湊值不符合要求")
                return False
                
            # 驗證區塊內所有交易
            for tx in block.transactions:
                if not any(party.verify_transaction(tx) for party in self.parties):
                    logger.warning(f"區塊 {block.index} 包含無效交易")
                    return False
                    
            # 驗證區塊連結
            if block.index > 0:
                prev_block = self.blockchain[block.index - 1]
                if block.previous_hash != prev_block.hash:
                    logger.warning(f"區塊 {block.index} 與前一個區塊連結無效")
                    return False
                    
            logger.debug(f"區塊 {block.index} 驗證成功")
            return True
        except Exception as e:
            logger.error(f"區塊驗證失敗：{str(e)}")
            return False

    def mine_block(self) -> Optional[Block]:
        if len(self.blockchain) >= self.max_blocks:
            logger.info("已達到最大區塊數量限制")
            return None
            
        transactions = self.transaction_pool[:self.max_transactions_per_block]
        
        # 根據 IP 地址選擇礦工
        miner = min(
            self.parties,
            key=lambda p: int(ipaddress.IPv4Address(p.ip.split('/')[0]))
        )
        
        new_block = Block(
            len(self.blockchain),
            self.blockchain[-1].hash,
            transactions,
            int(time.time())
        )
        
        logger.info(f"礦工 {miner.name} (IP: {miner.ip}) 開始挖礦區塊 {new_block.index}...")
        success, attempts = new_block.mine(self.mining_timeout)
        
        if success:
            if self.verify_block(new_block):
                self.transaction_pool = self.transaction_pool[len(transactions):]
                self.last_block_time = time.time()
                logger.info(f"區塊 {new_block.index} 挖礦並驗證成功")
                return new_block
            else:
                logger.warning(f"區塊 {new_block.index} 驗證失敗")
                return None
        else:
            logger.warning(f"區塊 {new_block.index} 挖礦失敗")
            return None

    def add_block(self, block: Block) -> bool:
        """
        手動添加新區塊到區塊鏈
        """
        try:
            logger.info(f"嘗試添加區塊 {block.index} 到區塊鏈")
            
            # 驗證區塊
            if not self.verify_block(block):
                logger.warning(f"區塊 {block.index} 驗證失敗，無法添加")
                return False
                
            # 檢查區塊索引是否正確
            if block.index != len(self.blockchain):
                logger.warning(f"區塊索引不正確：期望 {len(self.blockchain)}，實際 {block.index}")
                return False
                
            # 檢查前一個區塊的雜湊值
            if block.index > 0 and block.previous_hash != self.blockchain[-1].hash:
                logger.warning(f"區塊 {block.index} 的前一個雜湊值不匹配")
                return False
                
            # 添加區塊
            self.blockchain.append(block)
            self.total_blocks += 1
            self.last_block_time = time.time()
            
            # 從交易池中移除已包含的交易
            for tx in block.transactions:
                self.transaction_pool = [t for t in self.transaction_pool if t != tx]
            
            logger.info(f"成功添加區塊 {block.index} 到區塊鏈")
            return True
            
        except Exception as e:
            logger.error(f"添加區塊時發生錯誤：{str(e)}")
            return False

    def validate_chain(self) -> Tuple[bool, str]:
        """
        驗證整個區塊鏈的有效性
        返回：(是否有效, 錯誤訊息)
        """
        try:
            logger.info("開始驗證區塊鏈...")
            
            # 檢查是否為空
            if not self.blockchain:
                return False, "區塊鏈為空"
                
            # 檢查創世區塊
            genesis_block = self.blockchain[0]
            if genesis_block.index != 0 or genesis_block.previous_hash != "0" * 64:
                return False, "創世區塊無效"
                
            # 驗證每個區塊
            for i in range(1, len(self.blockchain)):
                current_block = self.blockchain[i]
                previous_block = self.blockchain[i-1]
                
                # 檢查區塊索引
                if current_block.index != i:
                    return False, f"區塊 {i} 的索引不正確"
                    
                # 檢查前一個區塊的雜湊值
                if current_block.previous_hash != previous_block.hash:
                    return False, f"區塊 {i} 的前一個雜湊值不匹配"
                    
                # 驗證區塊本身
                if not self.verify_block(current_block):
                    return False, f"區塊 {i} 驗證失敗"
                    
            logger.info("區塊鏈驗證成功")
            return True, "區塊鏈有效"
            
        except Exception as e:
            error_msg = f"驗證區塊鏈時發生錯誤：{str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def run(self):
        logger.info("開始運行區塊鏈模擬器...")
        start_time = time.time()
        
        try:
            while len(self.blockchain) < self.max_blocks:
                # 隨機選擇一個參與者生成交易
                party = random.choice(self.parties)
                receiver = random.choice([p for p in self.parties if p != party])
                value = random.randint(1, 100)
                
                # 創建並廣播交易
                transaction = party.create_transaction(receiver.name, value)
                if transaction:
                    self.transaction_pool.append(transaction)
                    self.total_transactions += 1
                    logger.debug(f"新交易已加入交易池：{transaction.to_dict()}")
                
                # 檢查是否應該挖礦
                if self.should_mine_block():
                    new_block = self.mine_block()
                    if new_block:
                        if self.add_block(new_block):
                            logger.info(f"區塊 {new_block.index} 已添加到區塊鏈")
                
                # 定期驗證區塊鏈
                if random.random() < 0.1:  # 10% 的機率進行驗證
                    is_valid, message = self.validate_chain()
                    if not is_valid:
                        logger.warning(f"區塊鏈驗證失敗：{message}")
                
                # 隨機延遲 1-16 秒
                delay = random.uniform(1, 16)
                logger.debug(f"等待 {delay:.2f} 秒...")
                time.sleep(delay)
            
            total_time = time.time() - start_time
            logger.info(f"區塊鏈模擬完成！總耗時：{total_time:.2f}秒")
            logger.info(f"總交易數：{self.total_transactions}")
            logger.info(f"總區塊數：{self.total_blocks}")
            
            # 最終驗證
            is_valid, message = self.validate_chain()
            logger.info(f"最終區塊鏈驗證結果：{message}")
            
            # 輸出最終區塊鏈
            print("\n最終區塊鏈：")
            for block in self.blockchain:
                print(json.dumps(block.to_dict(), indent=4, ensure_ascii=False))
                
        except KeyboardInterrupt:
            logger.info("使用者中斷執行")
        except Exception as e:
            logger.error(f"執行時發生錯誤：{str(e)}")
            raise

def main():
    print("=== 區塊鏈模擬器啟動 ===", flush=True)
    
    parser = argparse.ArgumentParser(description='區塊鏈模擬器')
    parser.add_argument('--debug', action='store_true', help='啟用除錯模式')
    parser.add_argument('--parties', type=int, default=5, help='參與者數量')
    args = parser.parse_args()
    
    try:
        print(f"參數設置：debug={args.debug}, parties={args.parties}", flush=True)
        
        if args.debug:
            logger.setLevel(logging.DEBUG)
            print("已啟用除錯模式", flush=True)
        
        print("正在初始化區塊鏈模擬器...", flush=True)
        
        simulator = BlockchainSimulator(args.parties, args.debug)
        print("初始化完成，開始運行...", flush=True)
        
        simulator.run()
        
        print("\n=== 模擬結束 ===", flush=True)
        print(f"總區塊數：{simulator.total_blocks}", flush=True)
        print(f"總交易數：{simulator.total_transactions}", flush=True)
        
        # 輸出最終區塊鏈
        print("\n最終區塊鏈：", flush=True)
        for block in simulator.blockchain:
            block_json = json.dumps(block.to_dict(), indent=4, ensure_ascii=False)
            print(block_json, flush=True)
            print("-" * 80, flush=True)
            
    except Exception as e:
        print(f"錯誤：{str(e)}", flush=True)
        logger.error(f"程式執行失敗：{str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("程式開始執行...", flush=True)
    main() 