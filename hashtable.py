from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    ''' Represent a Hashtable'''
    # polynomial constant, used for _hash
    P_CONSTANT = 37
    # Tuple stores information: (key, value, is_deleted)
    initial_tuple = (None, None, True)

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        '''Initialize an emppty list of capacity size'''
        self._items = [self.initial_tuple] * capacity
        self.capacity = capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.loaded_record = 0

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value
        between 0 and self.capacity.

        The particular function uses Horner's rule to compute large polynomial.
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity

    def __setitem__(self, key, val):
        '''Add or update key-value pair to the table'''
        index = self._hash(key)
        # Increase load count.
        self.loaded_record += 1
        while self._items[index] != self.initial_tuple:
            # Current index place has been used.
            if self._items[index][0] == key:
                # Update old key-value, shouldn't increase count.
                self.loaded_record -= 1
                break
            else:
                # Place is taken for other record.
                index = (index + 1) % self.capacity
        # Find available index place for the record.
        self._items[index] = (key, val, False)
        if self.loaded_record / self.capacity > self.load_factor:
            # Loaded beyond load_factor, do rehashing
            self.rehashing()
        return

    def __getitem__(self, key):
        '''Get key-value pair with given key'''
        index = self._hash(key)
        searched = 1
        while searched != self.capacity:
            if self._items[index] == self.initial_tuple:
                # Place available but not used, key doesn't exist
                return self.default_value
            elif self._items[index][0] != key:
                # Which means Not Found at current index place.
                # Tour next index.
                index = (index + 1) % self.capacity
                searched += 1
            elif self._items[index][2] is True:
                # Key already deleted
                return self.default_value
            else:
                # Found at hashed index place, return the value.
                return self._items[index][1]

    def __delitem__(self, key):
        '''Delete key-value pair with given key from the table'''
        index = self._hash(key)
        searched = 1
        while searched != self.capacity:
            if self._items[index] == self.initial_tuple:
                # Place available but not used, key doesn't exist
                raise KeyError
            elif self._items[index][0] != key:
                # Which means Not Found at current index place.
                # Tour next index.
                index = (index + 1) % self.capacity
                searched += 1
            elif self._items[index][2] is True:
                # Key already deleted
                raise KeyError
            else:
                # Found at hashed index place, return the value.
                self._items[index] = self._items[index][:2] + (True,)
                self.loaded_record -= 1
                return

    def __len__(self):
        '''Return length of the table (only valid records)'''
        return self.loaded_record

    def __iter__(self):
        """
        No need to implement __iter__ for this system.
        This stub is needed to satisfy `MutableMapping` however.)
        """
        raise NotImplementedError("__iter__ not implemented")

    def rehashing(self):
        '''Expand the table size and reload all key-value pairs'''
        # Get all valid previous key-value to new table.
        old_items = [(key, value) for key, value, is_deleted in self._items
                     if is_deleted is False]
        self.capacity *= self.growth_factor
        # Initiate a new empty table of new capacity.
        self._items = [self.initial_tuple] * self.capacity
        # Reset loaded record to 0.
        self.loaded_record = 0
        # Reload all old key-value.
        for key, value in old_items:
            self[key] = value
