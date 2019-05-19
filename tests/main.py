import sys
import os
import json

sys.path.append('../')
from pymap import ScannerHandler

with open('../input-files/hosts.json', 'r') as f:
    host_defs = json.loads(f.read())

scanner = ScannerHandler(host_defs)
scanner.scan()
print (scanner.get_dict())
