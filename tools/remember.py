class Memory:
    def __init__(self):
        self.storage = {}
    
    def store(self, key, value):
        """Store a value with a given key"""
        self.storage[key] = value
    
    def retrieve(self, key):
        """Retrieve a value by its key"""
        return self.storage.get(key)
    
    def forget(self, key):
        """Remove a value from memory"""
        if key in self.storage:
            del self.storage[key]
    
    def clear(self):
        """Clear all stored memories"""
        self.storage.clear()