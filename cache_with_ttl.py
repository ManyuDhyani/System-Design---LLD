# Hint: This is a leetcode question LRU with ttl(time to live)
import time

class ListNode:
    def __init__(self, key, val, ttl):
        self.key = key
        self.val = val
        self.expiry = time.time() + ttl if ttl else None
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.left = ListNode(0, 0, 0)  # dummy head
        self.right = ListNode(0, 0, 0) # dummy tail
        self.left.next = self.right
        self.right.prev = self.left
    
    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev
    
    def _insert(self, node):
        prev = self.right.prev
        node.next = self.right
        node.prev = prev
        self.right.prev = node
        prev.next = node

    def _is_expired(self, node):
        return node.expiry is not None and time.time() > node.expiry

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            if self._is_expired(node):
                self._remove(node)
                del self.cache[key]
                return -1
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int, ttl: int = 0) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
            del self.cache[key]
        
        new_node = ListNode(key, value, ttl)
        self.cache[key] = new_node
        self._insert(new_node)

        # Cleanup LRU if over capacity
        while len(self.cache) > self.cap:
            lru = self.left.next
            if self._is_expired(lru):
                self._remove(lru)
                del self.cache[lru.key]
            else:
                self._remove(lru)
                del self.cache[lru.key]
                break
