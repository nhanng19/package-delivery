class HashMap:
    """
    Hash map implementation
    """
    def __init__(self, size=100):    
        """
        Initializes the HashMap.
        Args: 
            size (int): The number of key value pairs
        Returns:
            None
        """
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def set(self, key, value):
        """    
        Add or update a key value pair.
        Args: 
            key: unique identifier 
            value: value stored for each unique key
        Returns: 
            bool
        """
        bucket_index = hash(key)
        bucket = self.buckets[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return True

        bucket.append((key, value))
        return True

    def get(self, key):
        """    
        Given the key, return the associated value.
        Args: 
            key: unique identifier 
        Returns: 
            The value of the key, or None if key isn't found.
        """
        bucket_index = hash(key)
        bucket = self.buckets[bucket_index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """    
        Delete a key value pair from the HashMap
        Args: 
            key: unique identifier 
        Returns: 
            True if the pair was successfully removed, False if the key wasn't found.
        """
        bucket_index = hash(key)
        bucket = self.buckets[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True

        return False
