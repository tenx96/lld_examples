from typing import Dict
from collections import OrderedDict, defaultdict


class Cache:
    def __init__(self, limit=10):
        self.limit = limit
        self.counter = 0
        self.map: Dict[str, (str, int)] = {}  # keys --> val, count
        self.min_freq = 1
        self.frequency_map = defaultdict(OrderedDict)  # freq_count --> [keys]

    def get(self, key: str):
        if key not in self.map:
            return -1

        val, ctr = self.map[key]

        # update ctr
        self.incr_key(ctr, key, val)

        return val

    def incr_key(self, curr_count, key, value):
        self.frequency_map[curr_count].pop(key)
        self.frequency_map[curr_count + 1].update({key: -1})  # dummy value
        self.frequency_map[curr_count + 1].move_to_end(key)
        self.map[key] = (value, curr_count + 1)

        if curr_count == self.min_freq and not self.frequency_map[curr_count]:
            self.min_freq += 1

    def set(self, key: str, val: str):
        if self.limit == 0:
            return

        if key not in self.map and self.counter == self.limit:
            self.evict_one_lfu()

        if key in self.map:
            _, c = self.map[key]
            self.incr_key(c, key, val)
        else:
            self.map[key] = (val, 1)
            self.frequency_map[1][key] = -1
            self.frequency_map[1].move_to_end(key)
            self.min_freq = 1
            self.counter += 1

    def evict_one_lfu(self):
        keys = self.frequency_map[self.min_freq]
        k, _ = keys.popitem(last=False)
        print(f"Evicting key {k}")
        del self.map[k]
        self.counter -= 1

        if not keys:
            del self.frequency_map[self.min_freq]


cac = Cache(limit=2)

cac.set("foo", "bar")
cac.set("f", "u")
cac.set("foo2", "333333") # foo gets evicted as max is 2

print(cac.get("foo"))
print(cac.get("foo2"))
print(cac.get("f"))
