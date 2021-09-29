"""Appends /src/tidyhome to path so that tidyhome.py can be imported to /srctest/ for unit-testing"""
import os
import sys
import inspect

# Generate string for full path to directory where this file is running
# and replace forward slash (/) with os-specific path separator
thisdir = os.path.dirname(__file__)

old = "srctest"

new = "src" + os.sep + "tidyhome"

tidydir = thisdir.replace(old, new)

sys.path.append(tidydir)