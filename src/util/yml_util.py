from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .attr_dict import AttrDict


class YmlUtil:
    @staticmethod
    def load(path):
        with open(f'{path}', 'rb') as handle:
            data = load(handle, Loader=Loader)
            print(data)
            return AttrDict.from_nested_dicts(data)
