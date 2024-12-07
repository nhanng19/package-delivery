class HashMap:
    def __init__(self, size=100):
        """
        Initialize the hash table with a specified size.
        Each slot in the table is a list to handle collisions using chaining.
        """
        self.size = size
        self.list = [[] for _ in range(size)]

    def set(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item # Update existing key
                return True
        
        key_value = [key, item]
        bucket_list.append(key_value) # Insert new key-value pair
        return True

    def get(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1] # Return the value associated with the key
        return None # Key not found

    def delete(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
 
        for kv in bucket_list:
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])