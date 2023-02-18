###############################################################################
# _env_init.py
# Author: Tom Kerr AB3GY
#
# Script to set the runtime environment for custom amateur radio applications.
# Enforces use of Python 3 and sets a local package path.
# Designed for personal use by the author, but freely available to anyone.
###############################################################################

### LOCAL CUSTOMIZATION ###
# Set this path to point to the custom amateur radio packages on this computer.
LOCAL_PACKAGE_PATH = r'D:\dev\AB3GY\pypkg'

# System level packages.
from importlib import util
import sys

# Check for proper Python version.
major_ver = sys.version_info[0]
minor_ver = sys.version_info[1]
micro_ver = sys.version_info[2]
if (major_ver < 3):
    print('Python version: ' + str(major_ver) + '.' + str(minor_ver) + '.' + str(micro_ver))
    print('Error: Python major version must be 3.x.x or greater.')
    sys.exit(1)

# Check to see if we can find a local package.
# If not, then set the local package path.
module_spec = util.find_spec('pyRigCat')
if module_spec is None:
    sys.path.insert(0, LOCAL_PACKAGE_PATH)

