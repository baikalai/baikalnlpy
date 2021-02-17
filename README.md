# What is this?

`deeqnlpy` is the python 3 library for deeq NLP.

Deeq(pronounce as deeque) NLP is a Korean NLP,
which provides tokenizing, POS tagging for Korean.

## How to install

```shell
pip3 install deeqnlpy
```

## How to use

```python
from deeqnlpy import Tagger

tagger = Tagger('localhost')

res = tagger.tags(["안녕하세요.", "반가워요!"])

j = res.as_json()

res.pos()
```
