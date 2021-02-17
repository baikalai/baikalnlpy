import grpc

import baikal.language.language_service_pb2 as pb
import baikal.language.language_service_pb2_grpc as ls

MAX_MESSAGE_LENGTH = 100 * 1024 * 1024


class DeeqLanguageServiceClient:

    stub = None

    def __init__(self, remote: str):
        channel = grpc.insecure_channel(
            remote,
            options=[
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
            ])

        self.stub = ls.LanguageServiceStub(channel)

    def analyze_syntax(self, content: str, domain: str = None, auto_split=False) -> pb.AnalyzeSyntaxResponse:
        req = pb.AnalyzeSyntaxRequest()
        # req.document = pb.Document()
        req.document.content = content
        req.document.language = "ko_KR"
        req.encoding_type = pb.EncodingType.UTF32
        req.auto_split_sentence = auto_split
        if domain is not None:
            req.custom_domain = domain
        try:
            res = self.stub.AnalyzeSyntax(req)
            return res
        except grpc.RpcError as e:
            print(e)
            return pb.AnalyzeSyntaxResponse()
