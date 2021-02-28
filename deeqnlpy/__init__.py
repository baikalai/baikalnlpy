"""
DeeqNLPy
=====
Provides
  1. a Korean Part-Of-Speech Tagger as deeq NLP client
  2. Multiple custom dictionaries which is kept in the your deeq NLP server.


How to use the documentation
----------------------------
Full documentation for deeq NLP is available in
installable tarball or docker images.
- see `docs/intro.html` at installable tarball.
- or `http://localhost:5757/intro.html` after running docker.

The docstring examples assume that `deeqnlpy` has been imported as `dn`::
  >>> import deeqnlpy as dn

Use the built-in ``help`` function to view a class's docstring::
  >>> help(dn.Tagger)
  ...

Classes
-------
Tagger
    the deeq NLP POS tagger for Korean
    `from deeqnlpy import Tagger`
Tagged
    Wrapper for tagged output
    `from deeqnlpy import Tagged`
CustomDict
    Custom dictionary for Korean.
    `from deeqnlpy import CustomDict`

Version
-------
```
import deeqnlpy as dn
print(dn.version)
print(dn.deeq_nlp_version)
```

Get deeq NLP
----------------------------
- Use docker, https://hub.docker.com/r/baikalai/deeq-nlp
- Or use a google form,
 https://docs.google.com/forms/d/e/1FAIpQLSfSJQCMwm0pS1nJiirwUNjfj-7jT-T_CLUfgMc-vTpRbHZZnw/viewform
"""

import sys
import os

_pb_ = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.insert(0, _pb_)

from deeqnlpy._tagger import Tagger, Tagged
from deeqnlpy._custom_dict import CustomDict
from deeqnlpy._custom_dict_client import CustomDictionaryServiceClient
from deeqnlpy._lang_service_client import DeeqLanguageServiceClient

version = "0.9"
deeq_nlp_version = "1.4.2"
