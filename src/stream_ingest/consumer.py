"""The Python implementation of the ingestion.Broker client: Consumer."""

from __future__ import print_function

import logging

import grpc
import typer
import stream_ingest.ingestion_pb2 as ingestion_pb2
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer(invoke_without_command=True)

@app.callback(invoke_without_command=True)
def main(number_of_messages: int = typer.Argument(1, help="Number of messages to pull")):
    """Pull messages from the Broker.

    Call as `pull-message 2` to pull 2 messages.
    """
    logger.info("Will try to pull simple message as Consumer...")

    channel = grpc.insecure_channel('localhost:50051')  # Keep open
    try:
        stub = ingestion_pb2_grpc.BrokerStub(channel)
        request = ingestion_pb2.PullRequest(number_of_messages=number_of_messages)
        responses = list(stub.PullMessage(request))
        
        if len(responses) == 0:
            logger.info("No messages received from Broker.")
        else:
            for r in responses:
                logger.info(f"Consumer received:\n {r}")
    finally:
        channel.close()

# def run():
#     """Console entry point used by the package script. Invokes the Typer app."""
#     app()

if __name__ == "__main__":
    app()