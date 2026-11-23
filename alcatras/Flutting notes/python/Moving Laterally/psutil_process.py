# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "psutil",
# ]
# ///

import psutil

p = psutil.Process()
available_attrs = list(p.as_dict().keys())
print(available_attrs)