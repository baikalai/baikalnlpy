# What is this?

`deeqnlpy` is the python 3 library for deeq NLP.

Deeq(pronounce as deeque) NLP is a Korean NLP,
which provides tokenizing, POS tagging for Korean.

## How to install

```shell
pip3 install deeqnlpy
```

## How to get deeq NLP
- Click [this form](https://docs.google.com/forms/d/e/1FAIpQLSfSJQCMwm0pS1nJiirwUNjfj-7jT-T_CLUfgMc-vTpRbHZZnw/viewform)
- Fill it.
- Get emailed download link, a license file.
- Or use docker image.
```shell
docker pull baikalai/deeq-nlp:v1.4.2
```
- Caution: You should use deeq NLP v1.4.2 or later.

## How to use

```python
import sys
import google.protobuf.text_format as tf
from deeqnlpy import Tagger

my_tagger = Tagger('localhost') # If you have your own local deeq NLP. 
# or
tagger = Tagger() # With smaller public cloud instance, it may be slow.

# print results. 
res = tagger.tags(["안녕하세요.", "반가워요!"])

# get protobuf message.
m = res.msg()
tf.PrintMessage(m, out=sys.stdout, as_utf8=True)
print(tf.MessageToString(m, as_utf8=True))
print(f'length of sentences is {len(m.sentences)}')
## output : 2
print(f'length of tokens in sentences[0] is {len(m.sentences[0].tokens)}')
print(f'length of morphemes of first token in sentences[0] is {len(m.sentences[0].tokens[0].morphemes)}')
print(f'lemma of first token in sentences[0] is {m.sentences[0].tokens[0].lemma}')
print(f'first morph of first token in sentences[0] is {m.sentences[0].tokens[0].morphemes[0]}')
print(f'tag of first morph of first token in sentences[0] is {m.sentences[0].tokens[0].morphemes[0].tag}')
# print number

# get json object
jo = res.as_json()
print(jo)

# get tuple of pos tagging.
pa = res.pos()
print(pa)
# another methods
ma = res.morphs()
print(ma)
na = res.nouns()
print(na)
va = res.verbs()
print(va)

# custom dictionary
cust_dic = tagger.custom_dict("my")
cust_dic.copy_np_set({'내고유명사', '우리집고유명사'})
cust_dic.copy_cp_set({'코로나19'})
cust_dic.copy_cp_caret_set({'코로나^백신', '"독감^백신'})
cust_dic.update()

tagger.set_domain('my')
tagger.pos('코로나19는 언제 끝날까요?')
```
