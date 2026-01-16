
"""The Python implementation of the ingestion.Broker client: Producer."""

from __future__ import print_function

from datetime import datetime
import structlog
from stream_ingest.config import configure_logging

import grpc
import typer
import stream_ingest.ingestion_pb2 as ingestion_pb2
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc

configure_logging()
logger = structlog.get_logger()
app = typer.Typer(invoke_without_command=True)

@app.callback(invoke_without_command=True)
def run(
    topic_name: str = typer.Argument("topic-1", help="Topic name to push messages to"),
    partition_id: int = typer.Argument(0, help="Partition ID to push messages to"),
    msg: str = typer.Argument("Hello, World!", help="Payload of the message to push")
    ):

    logger.info("Will try to push simple message as Producer...")

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        request = ingestion_pb2.PushRequest(topic_name=topic_name,
                                            payload=msg,
                                            partition_id=partition_id,
                                            timestamp=int(datetime.now().timestamp())
                                            )
        try:
            response = stub.PushMessage(request)
            if response.success:
                logger.info(f"Success: {response.message}")
            else:
                logger.error(f"Failed: {response.message}")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.code()} - {e.details()}")


if __name__ == "__main__":
    app()