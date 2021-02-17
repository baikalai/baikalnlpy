from typing import List

import grpc
from google.protobuf.empty_pb2 import Empty

import deeqnlpy.baikal.language.custom_dict_pb2 as pb
import deeqnlpy.baikal.language.custom_dict_pb2_grpc as cds
import deeqnlpy.baikal.language.dict_common_pb2 as common


def build_dict_set(domain: str, name: str, dict_set: set) -> common.DictSet:
    """
    make a DictSet message using domain, name, and dict_set
    :param domain: the domain name of dict_set
    :param name: name is built-in use only, which is fixed as one of 'np-set', 'cp-set', 'cp-caret'.
    :param dict_set: user provided set of custom dictionary.
    :return: made DictSet data
    """
    ret = common.DictSet()
    ret.name = domain + "-" + name
    ret.type = common.DictType.WORD_LIST
    for v in dict_set:
        ret.items[v] = 1
    return ret


class CustomDictionaryServiceClient:
    """
    The custom dictionary client which can create, update, list, delete your own one.
    커스텀 사전을 생성, 조회, 업데이트, 삭제하는 클라이언트
    """
    stub = None

    def __init__(self, remote):
        super().__init__()
        channel = grpc.insecure_channel(remote)
        self.stub = cds.CustomDictionaryServiceStub(channel)

    def get_list(self) -> List[pb.CustomDictionaryMeta]:
        req = Empty()
        try:
            res = self.stub.GetCustomDictionaryList(req)
            return res.domain_dicts
        except grpc.RpcError as e:
            print(e)
            return []

    def get(self, domain: str) -> pb.CustomDictionary:
        req = pb.GetCustomDictionaryRequest()
        req.domain_name = domain
        try:
            res = self.stub.GetCustomDictionary(req)
            return res.dict
        except grpc.RpcError as e:
            print(e)
            return None

    def update(self, domain: str, np: set, cp: set, cp_caret: set) -> bool:
        """
        Update custom dictionary.
        :param domain: domain name of these custom dictionaries.
        :param np: proper noun set
        :param cp: compound noun set
        :param cp_caret: splittable compound noun set
        :return: if successfully updated return true
        """
        req = pb.UpdateCustomDictionaryRequest()
        req.domain_name = domain

        req.dict.domain_name = domain

        req.dict.np_set.CopyFrom(build_dict_set(domain, 'np-set', np))
        req.dict.cp_set.CopyFrom(build_dict_set(domain, 'cp-set', cp))
        req.dict.cp_caret_set.CopyFrom(build_dict_set(domain, 'cp-caret-set', cp_caret))

        try:
            res = self.stub.UpdateCustomDictionary(req)
            return res.updated_domain_name == domain
        except grpc.RpcError as e:
            print(e)
            return False

    def remove_all(self) -> List[str]:
        """
        모든 커스텀 사전을 삭제한 이후에 반환한다.
        :return: 삭제된 도메인의 이름들
        """
        req = pb.RemoveCustomDictionariesRequest()
        req.all = True

        try:
            res = self.stub.RemoveCustomDictionaries(req)
            return res.deleted_domain_names.keys()
        except grpc.RpcError as e:
            print(e)
            return []

    def remove(self, domains: List[str]) -> List[str]:
        """
        지정한 도메인의 커스텀 사전을 삭제한다.
        :param domains: 삭제할 커스텀 사전의 도메인의 배열들
        :return: 정상 삭제 여부
        """
        req = pb.RemoveCustomDictionariesRequest()
        req.domain_names.extend(domains)
        req.all = False
        try:
            res = self.stub.RemoveCustomDictionaries(req)
            return res.deleted_domain_names.keys()
        except grpc.RpcError as e:
            print(e)
            return []
