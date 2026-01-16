
"""The Python implementation of the ingestion.Admin client."""

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

app = typer.Typer()

@app.command()
def add_topic(
    topic_name: str = typer.Argument("topic-name-1", help="Topic name to add"),
    partition_count: int = typer.Argument("1", help="Partition count for the topic"),
    replication_factor: int = typer.Argument("1", help="Replication factor for the topic")
    ):

    logger.info(f"Argument received: topic_name='{topic_name}', type={type(topic_name)}")
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logger.info("Will try to add a topic to Broker as Admin...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        request = ingestion_pb2.AddTopicRequest(topic_name=topic_name,
                                                partition_count=partition_count,
                                                replication_factor=replication_factor)
        logger.info(f"Adding topic with name='{request.topic_name}'")
        response = stub.AddTopic(request)
    logger.info("Admin received: " + response.message)

@app.command()
def list_topics():
    logger.info("Will try to list topics from Broker as Admin...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        request = ingestion_pb2.ListTopicsRequest()
        response = stub.ListTopics(request)
    logger.info("Admin received: " + str(response.topics))


def main() -> None:
    app()