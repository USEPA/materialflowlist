"""Set common variables for use in package."""
import sys
import os
import logging as log

try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'materialflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)