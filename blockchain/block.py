class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        
    def __repr__(self):
        return f"Block(index={self.index}, previous_hash='{self.previous_hash}', timestamp='{self.timestamp}', data={self.data})"