from urllib.parse import urlsplit, parse_qs
import pandas as pd
import math
import requests


class ResourceIterator:
    def __init__(self, api, resource, page_size=10, query={}):
        self.api            = api
        self.api_client     = api.api
        self.resource       = resource
        self.call           = getattr(api, resource)
        self.page_size      = page_size
        self.next_offset    = 0
        self.current_offset = 0
        self.total          = 0
        self.query          = query


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

        self.query['offset'] = self.next_offset
        self.query['limit']  = self.page_size

        # Bypass al bug de simple_rest_client usando la URL base dinámica del recurso
        resource_client = getattr(self.api_client, self.resource)
        url_base = resource_client.actions['pages']['url'].split('?')[0]
        url = f"{self.api_client.api_root_url}{url_base}"
        headers = self.api_client.headers
        
        response = requests.get(url, params=self.query, headers=headers)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
            
        page = response.json()

        self.total = int(page['count'])


        if not page['results']:
            self.next_offset = None
            self.current_offset += self.page_size
        elif page['next']:
            params = parse_qs(urlsplit(page['next']).query)
            new_offset = int(params['offset'][0])
            # Blindaje contra bucle circular:
            if new_offset <= self.next_offset:
                self.next_offset = None
                self.current_offset += self.page_size
            else:
                self.next_offset    = new_offset
                self.current_offset = self.next_offset - self.page_size
        else:
            self.next_offset    = None
            self.current_offset += self.page_size

        return page['results']
