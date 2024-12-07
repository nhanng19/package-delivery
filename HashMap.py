class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.list = [[] for _ in range(size)]

    def set(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def get(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def delete(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
 
        for kv in bucket_list:
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])