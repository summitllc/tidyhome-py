"""Appends /src/tidyhome to path so that tidyhome.py can be imported to /srctest/ for unit-testing"""
import os
import sys
import inspect

# Generate string for full path to directory where this file is running
# and replace forward slash (/) with os-specific path separator
thisdir = inspect.stack()[0][1].replace('/', os.sep)

old = "srctest" + os.sep + "append_src_tidyhome.py"

new = "src" + os.sep + "tidyhome"

tidydir = thisdir.replace(old, new)

sys.path.append(tidydir)
