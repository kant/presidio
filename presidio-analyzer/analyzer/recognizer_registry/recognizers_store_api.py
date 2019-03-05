import logging

import grpc
import recognizers_store_pb2
import recognizers_store_pb2_grpc


class RecognizerStoreApi:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:3004')
        self.rs_stub = recognizers_store_pb2_grpc.RecognizersStoreServiceStub(
            channel)

    def get_latest_timestamp(self):
        timestamp_request = \
            recognizers_store_pb2.RecognizerGetTimestampRequest()
        lst_update = 0
        try:
            lst_update = self.rs_stub.ApplyGetTimestamp(
                timestamp_request).unixTimestamp
        except grpc.RpcError:
            logging.info("Failed to get timestamp")
            return 0
        return lst_update

    def get_all_recognizers(self):
        req = recognizers_store_pb2.RecognizersGetAllRequest()
        return self.rs_stub.ApplyGetAll(req).recognizers
