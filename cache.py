import sys
import re
from hash_table import HashTable 


# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!
class CacheItem:
    def __init__(self,url,contents):
        self.url = url
        self.contents = contents
        self.next = None
        self.prev = None

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):　　　　#HashTableと連結リストの組み合わせ
        self.hash_table = HashTable()
        self.cache_size = n
        self.head = None
        self.tail = None


    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        
        domain_parts = url.split('.')
        url_key = domain_parts[0]
        cached_item, found = self.hash_table.get(url_key)

        if not found:    #cacheにない値だったら
            new_item = CacheItem(url ,contents)
            self.hash_table.put(url_key ,contents)

            if self.head == None and self.tail == None: #cacheが空だった場合
                self.head = new_item
                self.tail = new_item
            else:
                if self.hash_table.item_count > self.cache_size: #cacheの中が満タンで頭を消す必要がある場合
                    self.head = self.head.next
                    if self.head:
                        self.head.prev = None
                    keys  = self.head.url.split('.')
                    self.hash_table.delete(keys[0])
            
                new_item.prev = self.tail
                self.tail.next = new_item
                self.tail = new_item
        elif self.tail.url != url: #cacheにある値かつtailではないため、cacheの再構成が必要な場合
            current = self.tail
            while current:
                if current.url == url:
                    if current != self.head:
                       current.prev.next = current.next
                       current.next.prev = current.prev
                    else:
                        self.head = self.head.next
                        self.head.prev = None
                current = current.prev
            new_item = CacheItem(url ,contents)
            new_item.prev = self.tail
            self.tail.next = new_item
            self.tail = new_item
            

     
    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        url_list = []
        current = self.tail
        while current:
            url_list.append(current.url)
            current = current.prev
        
        return url_list


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)
    
    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
