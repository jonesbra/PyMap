import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))

from pymap import PyMap

p = PyMap()
p.scan()
