import sys
import os
import json

sys.path.append('../')
from pymap import Scanner

with open('../input-files/hosts.json', 'r') as f:
    host_defs = json.loads(f.read())

scanner = Scanner(host_defs=host_defs)
print (scanner.hosts)
