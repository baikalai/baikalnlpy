# -*- coding: utf-8 -*-

from ._custom_dict_client import CustomDictionaryServiceClient
from baikal.language.custom_dict_pb2 import CustomDictionary


def read_dic_file(fn):
    dict_set = set()
    with open(fn, 'r') as r:
        while True:
            w = r.readline()
            if not w:
                break
            if w[0] != '#':
                w2 = w.strip()
                if len(w2) > 0:
                    dict_set.add(w2)
    return dict_set


class CustomDict():
    """
    CustomDict Wrapper
    'CustomDict' .
    :ref:`optional-installations`.
    .. code-block:: python
        :emphasize-lines: 1
        >>> import deeqnlpy as dn
        >>> tagger = dn.Tagger()
        >>> cd = tagger.custom_dict("law")
        >>> # or
        >>> cd = dn.CustomDict("law", "localhost", 5656)
        >>> cd.read_cp_set_from_file("my_np_set.txt")
        >>> cd.copy_cp_set(set(['새단어', '코로나19', 'K방역']))
        >>> cd.read_cp_caret_set_from_file('my_cp_caret.txt')
        >>> cd.update()
        >>> ## copy data from server
        >>> cd2 = tagger.custom_dict("law")
        >>> custom_dict = cd2.get()
        >>> # cd2.save(dir="my_dir")

    :param domain       : str. domain of newly added custom dict.
                          There is no fixed name;
                          users can set use any words according to their needs. (example : "law")
    :param host         : str. host num
    :param port         : str. port num
    """

    domain = None
    stub = None
    cp_set = set()
    np_set = set()
    cp_caret_set = set()

    def __init__(self, domain: str, host: str = None, port: int = 5656):
        if host is None:
            host = 'nlp.deeq.ai'
        if port is None:
            port = 5656
        addr = host + ':' + str(port)
        self.domain = domain
        if domain is None:
            raise ValueError("domain name must be specified.")

        self.stub = CustomDictionaryServiceClient(addr)

    def read_np_set_from_file(self, fn: str):
        self.np_set = read_dic_file(fn)

    def read_cp_set_from_file(self, fn: str):
        self.cp_set = read_dic_file(fn)

    def read_cp_caret_set_from_file(self, fn: str):
        self.cp_caret_set = read_dic_file(fn)

    def copy_np_set(self, dict_set: set):
        self.np_set = dict_set

    def copy_cp_set(self, dict_set: set):
        self.cp_set = dict_set

    def copy_cp_caret_set(self, dict_set: set):
        """
        copy custom dictionary set for "compound noun".
        :param dict_set: set
        :return: None
        """
        self.cp_caret_set = dict_set

    def update(self):
        """
        update customized dictionary to deeq NLP server.
        :return: return True on success
        """
        return self.stub.update(self.domain,
                                self.np_set,
                                self.cp_set,
                                self.cp_caret_set)

    def get(self) -> CustomDictionary:
        """
        get custom dictionary from deeq NLP server.
        :return: CustomDictionary object.
        """
        return self.stub.get(self.domain)

    def clear(self):
        """
        clear loaded or copied custom dictionary set.
        :return:
        """
        self.np_set.clear()
        self.cp_set.clear()
        self.cp_caret_set.clear()
        return self.stub.remove([self.domain])

