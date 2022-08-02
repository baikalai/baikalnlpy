from typing import List

import grpc
from google.protobuf.empty_pb2 import Empty

import baikal.language.custom_dict_pb2 as pb
import baikal.language.custom_dict_pb2_grpc as cds
import baikal.language.dict_common_pb2 as common



def build_dict_set(domain: str, name: str, dict_set: set) -> common.DictSet:
    """
    주어진 파라미터를 사용하여 사용자 사전의 한 표현 형태인 DictSet protobuf 메시지를 만듭니다.

    Args:
        domain (str): 사용자 사전의 이름
        name (str): 사용자 사전에 대한 설명
        dict_set (set): 사용자 사전에 들어가야 할 단어들의 잡합

    Returns:
        common.DictSet: protobuf DictSet 메시지
    """
    ret = common.DictSet()
    ret.name = domain + "-" + name
    ret.type = common.DictType.WORD_LIST
    for v in dict_set:
        ret.items[v] = 1
    return ret


MAX_MESSAGE_LENGTH = 100 * 1024 * 1024


class CustomDictionaryServiceClient:
    """
    커스텀 사전을 생성, 조회, 업데이트, 삭제하는 클라이언트
    
    The custom dictionary client which can create, update, list, delete your own one.
    """

    def __init__(self, remote: str):
        """사용자 사전을 관리하는 클라이언트 객체 생성자

        Args:
            remote (str): 원격 주소, IP주소:포트 또는 호스트이름:포트 형식으로 사용합니다.
        """
        super().__init__()
        channel = grpc.insecure_channel(remote,
                                        options=[
                                            ('grpc.max_send_message_length',
                                             MAX_MESSAGE_LENGTH),
                                            ('grpc.max_receive_message_length',
                                             MAX_MESSAGE_LENGTH),
                                        ])
        self.stub = cds.CustomDictionaryServiceStub(channel)


    def get_list(self) -> List[pb.CustomDictionaryMeta]:
        """사전 목록을 가져옵니다.

        Raises:
            e: grpc.Error, 원격 호출시 예외가 발생할 수 있습니다.

        Returns:
            List[pb.CustomDictionaryMeta]: 사전에 대한 정보들을 목록을 배열합니다.
        """
        req = Empty()
        try:
            res = self.stub.GetCustomDictionaryList(req)
            return res.domain_dicts
        except grpc.RpcError as e:
            raise e


    def get(self, domain: str) -> pb.CustomDictionary:
        """
        정의된 사용사 사전의 내용 전체를 가져온다.

        Args:
            domain (str): 사용자 사전이 이름

        Raises:
            e: grpc.Error, 원격 호출시 예외가 발생할 수 있습니다.

        Returns:
            pb.CustomDictionary: 사용자 사전 데이터 전체를 담고 있는 protobuf 메시지
        """
        req = pb.GetCustomDictionaryRequest()
        req.domain_name = domain
        try:
            res = self.stub.GetCustomDictionary(req)
            return res.dict
        except grpc.RpcError as e:
            raise e


    def update(self, domain: str, np: set, cp: set, cp_caret: set) -> bool:
        """ 사용자 사전을 갱신합니다.

        Args:
            domain (str): 사용자 사전의 이름
            np (set): 고유명사 단어 집합
            cp (set): 복합명사 단어 집합
            cp_caret (set): 복합명사 분리 단어 집합

        Raises:
            e: grpc.Error, 원격 호출시 예외가 발생할 수 있습니다.

        Returns:
            bool: 정상적으로 갱신되면 참을 돌려줍니다.
        """
        
        req = pb.UpdateCustomDictionaryRequest()
        req.domain_name = domain

        req.dict.domain_name = domain

        req.dict.np_set.CopyFrom(build_dict_set(domain, 'np-set', np))
        req.dict.cp_set.CopyFrom(build_dict_set(domain, 'cp-set', cp))
        req.dict.cp_caret_set.CopyFrom(
            build_dict_set(domain, 'cp-caret-set', cp_caret))

        try:
            res = self.stub.UpdateCustomDictionary(req)
            return res.updated_domain_name == domain
        except grpc.RpcError as e:
            raise e


        """
        :return: 삭제된 도메인의 이름들
        """
    def remove_all(self) -> List[str]:
        """
        모든 커스텀 사전을 삭제한 다음 삭제한 사전의 이름을 돌려줍니다.

        Raises:
            e: grpc.Error, 원격 호출시 예외가 발생할 수 있습니다.

        Returns:
            List[str]: 삭제한 사전의 이름
        """
        req = pb.RemoveCustomDictionariesRequest()
        req.all = True

        try:
            res = self.stub.RemoveCustomDictionaries(req)
            return res.deleted_domain_names.keys()
        except grpc.RpcError as e:
            raise e

        """
        지정한 도메인의 커스텀 사전을 삭제한다.
        :param domains: 
        :return: 
        """
    def remove(self, domains: List[str]) -> List[str]:
        """ 지정한 도메인의 사용지 사전을 삭제한 다음 삭제한 사전의 목록을 반환합니다.

        Args:
            domains (List[str]): 삭제할 커스텀 사전의 이름들

        Raises:
            e: grpc.Error, 원격 호출시 예외가 발생할 수 있습니다.

        Returns:
            List[str]: 정상 삭제된 도메인의 이름 목록을 돌려줍니다.
        """
        req = pb.RemoveCustomDictionariesRequest()
        req.domain_names.extend(domains)
        req.all = False
        try:
            res = self.stub.RemoveCustomDictionaries(req)
            return res.deleted_domain_names.keys()
        except grpc.RpcError as e:
            raise e
