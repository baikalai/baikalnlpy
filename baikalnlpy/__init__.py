"""
BaikalNLPy
=====
Provides
  1. a Korean Part-Of-Speech Tagger as baikal NLP client
  2. Multiple custom dictionaries which is kept in the your baikal NLP server.


How to use the documentation
----------------------------
Full documentation for baikal NLP is available in
installable tarball or docker images.
- see `docs/intro.html` at installable tarball.
- or `http://localhost:5757/intro.html` after running docker.

The docstring examples assume that `baikalnlpy` has been imported as `bn`::
  >>> import baikalnlpy as bn

Use the built-in ``help`` function to view a class's docstring::
  >>> help(bn.Tagger)
  ...

Classes
-------
Tagger
    the baikal NLP POS tagger for Korean
    `from baikalnlpy import Tagger`
Tagged
    Wrapper for tagged output
    `from baikalnlpy import Tagged`
CustomDict
    Custom dictionary for Korean.
    `from baikalnlpy import CustomDict`

Version
-------
```
import baikalnlpy as bn
print(bn.version)
print(bn.baikal_nlp_version)
```

Get baikal NLP
----------------------------
- Use docker, https://hub.docker.com/r/baikalai/baikal-nlp
- Or download from https://license.baikal.ai/
"""

import sys
import os

from baikalnlpy._tagger import Tagger, Tagged
from baikalnlpy._custom_dict import CustomDict
from baikalnlpy._custom_dict_client import CustomDictionaryServiceClient
from baikalnlpy._lang_service_client import BaikalLanguageServiceClient

version = "1.0"
baikal_nlp_version = "1.7.3"
