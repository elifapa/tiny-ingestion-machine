
"""The Python implementation of the ingestion.Broker client: Producer."""

from __future__ import print_function

from datetime import datetime
import logging

import grpc
import stream_ingest.ingestion_pb2 as ingestion_pb2
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc

logger = logging.getLogger(__name__)

def run():
    logging.basicConfig(level=logging.INFO)
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logger.info("Will try to push simple message as Producer...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        response = stub.PushMessage(
            ingestion_pb2.PushRequest(id="test", payload="Hello, World!", timestamp=int(datetime.now().timestamp()))
            )
    logger.info("Broker client Producer received: " + response.message)


if __name__ == "__main__":
    run()