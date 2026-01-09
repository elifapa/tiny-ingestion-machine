from concurrent import futures
import logging

import grpc
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc
import stream_ingest.ingestion_pb2 as ingestion_pb2
from datetime import datetime

logger = logging.getLogger(__name__)

class Broker(ingestion_pb2_grpc.BrokerServicer):

    def PullMessage(self, request, context):
        # Implement the logic to pull messages from the broker
        for i in range(request.number_of_messages):
            response = ingestion_pb2.PullResponse(
                id=f"msg-{i}",
                payload=f"Payload for message {i}",
                timestamp=int(datetime.now().timestamp())
            )
            yield response

    def PushMessage(self, request, context):
        # Implement the logic to push messages to the broker
        logger.info(f"Received message with ID: {request.id} and payload: {request.payload}")
        response = ingestion_pb2.PushResponse(
            success=True,
            message="Message pushed successfully"
        )
        return response


def serve():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    port = "50051"
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    ingestion_pb2_grpc.add_BrokerServicer_to_server(Broker(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logger.info("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()