from urllib.parse import urlsplit, parse_qs
import pandas as pd
import math


def url_params(url): return parse_qs(urlsplit(url).query)


class ResourceIterator:
    def __init__(self, api, resource, page_size=5):
        self.call           = getattr(api, resource)
        self.page_size      = page_size
        self.next_offset    = 0
        self.current_offset = 0
        self.total          = 0


    @property
    def page(self): return int(self.current_offset / self.page_size) + 1

    @property
    def total_pages(self): return math.ceil(self.total/self.page_size)

    @property
    def count(self):
        count = int(self.page * self.page_size)
        return self.total if count > self.total else count

    
    def reset(self): self.next_offset = 0
    

    def __iter__(self):
        self.reset()
        return self


    def __next__(self):
        if self.next_offset is None:
            raise StopIteration            
        
        page = self.call(self.next_offset,  self.page_size).body
        
        params = url_params(page['next'])

        self.total = int(page['count'])


        if page['next']:
            self.next_offset    = int(params['offset'][0])
            self.current_offset = self.next_offset - self.page_size
        else:
            self.next_offset    = None
            self.current_offset += self.page_size
        
        return page['results']
