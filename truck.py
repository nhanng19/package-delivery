class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.list = [[] for _ in range(size)]

    def insert(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv_pairs in bucket_list:
            if kv_pairs[0] == key:
                kv_pairs[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        
        return True
    
    def retrieve(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv_pairs in bucket_list:
            if kv_pairs[0] == key:
                return kv_pairs[1]
        
        return None


