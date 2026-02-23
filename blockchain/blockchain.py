import hashlib
import json
from datetime import datetime
from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4
        self.mining_reward = 10
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(
            index=0,
            previous_hash='0',
            timestamp=datetime.now().isoformat(),
            data={'message': 'Genesis Block - SantochiCoin'}
        )
        genesis_block.hash = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def calculate_hash(self, block):
        """Calculate SHA-256 hash for a block"""
        block_string = json.dumps({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'data': str(block.data)
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def get_latest_block(self):
        """Get the last block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, sender, receiver, amount):
        """Add a pending transaction"""
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        self.pending_transactions.append(transaction)
        return len(self.chain) + 1
    
    def mine_block(self, miner_address):
        """Mine a new block with pending transactions"""
        if not self.pending_transactions:
            return False
        
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=datetime.now().isoformat(),
            data={
                'transactions': self.pending_transactions,
                'miner': miner_address
            }
        )
        
        # Proof of Work
        new_block.nonce = 0
        while not self.is_valid_proof(new_block):
            new_block.nonce += 1
        
        new_block.hash = self.calculate_hash(new_block)
        self.chain.append(new_block)
        
        # Add mining reward
        self.pending_transactions = [
            {'sender': 'SYSTEM', 'receiver': miner_address, 'amount': self.mining_reward}
        ]
        
        return True
    
    def is_valid_proof(self, block):
        """Check if block's hash meets difficulty requirement"""
        block_hash = self.calculate_hash(block)
        return block_hash.startswith('0' * self.difficulty)
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
            if current_block.hash != self.calculate_hash(current_block):
                return False
        
        return True
    
    def get_balance(self, address):
        """Get balance for an address"""
        balance = 0
        
        for block in self.chain:
            if isinstance(block.data, dict) and 'transactions' in block.data:
                for transaction in block.data['transactions']:
                    if transaction['sender'] == address:
                        balance -= transaction['amount']
                    if transaction['receiver'] == address:
                        balance += transaction['amount']
        
        return balance
