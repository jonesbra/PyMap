import sys
import os
import json

sys.path.append('../')
from pymap import ScannerHandler

with open('../input-files/hosts.json', 'r') as f:
    host_defs = json.loads(f.read())

scanner = ScannerHandler(host_defs)
scanner.scan()
data = scanner.get_dict()

print (json.dumps(scanner.get_dict(), indent=4))

with open('./out.json', 'w') as f:
    f.write(json.dumps(scanner.get_dict(), indent=4))
