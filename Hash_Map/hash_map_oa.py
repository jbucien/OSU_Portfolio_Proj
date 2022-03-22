# Name: Jenna Bucien
# OSU Email: bucienj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - Hash Map
# Due Date: 03.11.2022
# Description: Implementation of a hash table with open addressing and quadratic probing for collision resolution. Uses a DynamicArray as its underlying data structure. Methods of the HashMap class include: put(), get(), remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load(), get_keys().


from a6_include import *


class HashEntry:
    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ""
        for i in range(self.buckets.length()):
            out += str(i) + ": " + str(self.buckets[i]) + "\n"
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter. Calls quad_probe() to search the hash map for the key. If the key, returns its associated value. If the input key is not in the hash map, returns None.
        """
        # Get adjusted index
        index = self.quad_probe(key)
        # If there is nothing at the index, or the HashEntry is a tombstone, return False
        if self.buckets[index] is None:
            return None
        elif self.buckets[index].is_tombstone is True:
            return None
        else:
            return self.buckets[index].value

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and value as parameters. Calls quad_probe() to search the hash map for the key. If the input key already exists in the hash map, updates the key's associated value to the input value. If the input key is not already in the hash map, calls table_load(). If load factor is >= 0.5, calls resize_table() to increase the hash table capacity before adding the new key / value pair to the hash map.
        """
        # Determine if resize is needed:
        if self.table_load() >= 0.5:
            self.resize_table(2 * self.capacity)

        # Get new adjusted index
        index = self.quad_probe(key)

        # Determine if key is in array. If so, update value and tombstone status if needed
        if self.buckets[index] is not None:
            if self.buckets[index].is_tombstone is True:
                self.buckets[index].is_tombstone = False
            self.buckets[index].value = value
        else:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter. Locates the key's index using quad_probe()and removes it and its associated value from the hash map by changing the HashEntry's is_tombstone property to True. If the key is not in the hash map, the method returns without doing anything.
        """
        # Get adjusted index
        index = self.quad_probe(key)

        if self.buckets[index] is None:
            return
        elif self.buckets[index].is_tombstone is True:
            return
        else:
            self.buckets[index].is_tombstone = True
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter. Calls quad_probe() to search the hash map for the key and returns True if it is in the hash map; otherwise, returns False. An empty hash map does not contain any keys.
        """
        if self.size == 0:
            return False

        # Get adjusted index
        index = self.quad_probe(key)
        # If there is nothing at the index, or the HashEntry is a tombstone, return False
        if self.buckets[index] is None:
            return False
        elif self.buckets[index].is_tombstone is True:
            return False
        else:
            return True

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Returns the number of empty buckets currently in the hash table.
        """
        empty = 0
        for i in range(self.capacity):
            if self.buckets[i] is None:
                empty += 1
            elif self.buckets[i].is_tombstone is True:
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the current hash table load factor, or n/m, where n is the the total number of elements stored in the table (self.size) and m is the number of buckets (self.capacity).
        """
        return self.size / self.capacity

    def quad_probe(self, key: str) -> int:
        """
        Takes a key and the desired method names as parameters and calculates its initial index based on its load factor; then uses quadratic probing to return an adjusted index. The adjusted index will either be the key's location in the hash map, or the first empty space available.
        """
        # calculate initial_index
        hash = self.hash_function(key)
        in_index = hash % self.capacity

        # calculate adjusted index
        j = 0
        ad_index = in_index

        while True:
            ad_index = (in_index + j**2) % self.capacity
            if self.buckets[ad_index] is None:
                return ad_index
            elif (
                self.buckets[ad_index].key == key
                and self.buckets[ad_index].is_tombstone is False
            ):
                return ad_index
            else:
                j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer and changes the capacity of the internal hash table to that input integer. All existing key/value pairs remain in the new hash map, and all hash table links are rehashed. If the integer is less than 1 OR less than the current number of elements in the map, the method does nothing.
        """
        # check that new_capacity is valid
        if new_capacity < self.size:
            return

        # make a new HashMap to copy key/values into.
        new_hash = HashMap(new_capacity, self.hash_function)

        # for each bucket in the original
        for i in range(self.capacity):
            if self.buckets[i] is None:
                continue
            elif self.buckets[i].is_tombstone is True:
                continue
            else:
                new_hash.put(self.buckets[i].key, self.buckets[i].value)

        # copy new hash map and its attributes to the original
        self.buckets = new_hash.buckets
        self.capacity = new_hash.capacity
        self.size = new_hash.size
        self.hash_function = new_hash.hash_function

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters. Returns a DynamicArray that contains all the keys stored in the hash map. The order of the keys in the DA does not matter.
        """
        key_DA = DynamicArray()

        # for each bucket
        for i in range(self.capacity):
            if self.buckets[i] is None:
                continue
            elif self.buckets[i].is_tombstone is True:
                continue
            else:
                key_DA.append(self.buckets[i].key)
        return key_DA


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put("key1", 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put("key2", 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put("key1", 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put("key4", 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put("key" + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - put example 3")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(10, hash_function_1)
    m.put("key160", -245)
    m.put("key513", -159)
    m.put("key71", 18)
    m.put("key550", -336)
    m.put("key906", -87)
    m.put("key906", 13)
    print(m.capacity, m.size)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put("key1", 10)
    print(m.table_load())
    m.put("key2", 20)
    print(m.table_load())
    m.put("key1", 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put("key" + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key1", 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put("key1", 10)
    print(m.size, m.capacity)
    m.put("key2", 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put("str" + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put("str" + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key("key1"))
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key3", 30)
    print(m.contains_key("key1"))
    print(m.contains_key("key4"))
    print(m.contains_key("key2"))
    print(m.contains_key("key3"))
    m.remove("key3")
    print(m.contains_key("key3"))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get("key"))
    m.put("key1", 10)
    print(m.get("key1"))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get("key1"))
    m.put("key1", 10)
    print(m.get("key1"))
    m.remove("key1")
    print(m.get("key1"))
    m.remove("key4")

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put("key1", 10)
    print(m.size, m.capacity, m.get("key1"), m.contains_key("key1"))
    m.resize_table(30)
    print(m.size, m.capacity, m.get("key1"), m.contains_key("key1"))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put("some key", "some value")
        result = m.contains_key("some key")
        m.remove("some key")

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put("200", "2000")
    m.remove("100")
    m.resize_table(2)
    print(m.get_keys())
