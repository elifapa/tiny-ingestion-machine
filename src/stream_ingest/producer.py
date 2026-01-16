
"""The Python implementation of the ingestion.Broker client: Producer."""

from __future__ import print_function

from datetime import datetime
import logging

import grpc
import typer
import stream_ingest.ingestion_pb2 as ingestion_pb2
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc

logger = logging.getLogger(__name__)
app = typer.Typer(invoke_without_command=True)

@app.callback(invoke_without_command=True)
def run(msg: str = typer.Argument("Hello, World!", help="Payload of the message to push")):
    logging.basicConfig(level=logging.INFO)
    logger.info(f"Argument received: msg='{msg}', type={type(msg)}")
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logger.info("Will try to push simple message as Producer...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        request = ingestion_pb2.PushRequest(payload=msg, timestamp=int(datetime.now().timestamp()))
        logger.info(f"Pushing request with payload='{request.payload}'")
        response = stub.PushMessage(request)
    logger.info("Producer received: " + response.message)


if __name__ == "__main__":
    app()