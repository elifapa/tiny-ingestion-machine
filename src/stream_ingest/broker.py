from concurrent import futures
import logging

import grpc
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc
import stream_ingest.ingestion_pb2 as ingestion_pb2
from datetime import datetime
import queue
import uuid

logger = logging.getLogger(__name__)

class Broker(ingestion_pb2_grpc.BrokerServicer):

    def __init__(self):
        self.message_queue = queue.Queue()

    def PullMessage(self, request, context):
        # Pull messages from the queue in order
        pulled = 0
        while pulled < request.number_of_messages:
            try:
                message = self.message_queue.get(timeout=1)
                logger.info(f"Sent message with ID: {message['id']} and payload: {message['payload']}")

                response = ingestion_pb2.PullResponse(
                    id=message['id'],
                    payload=message['payload'],
                    timestamp=message['timestamp']
                )
                yield response
                pulled += 1
            except queue.Empty:
                logger.warning(f"Queue is empty, requested {request.number_of_messages} but only {pulled} messages available")
                break

    def PushMessage(self, request, context):
        # Store the message in the queue with a generated UUID
        message_id = str(uuid.uuid4())
        message = {
            'id': message_id,
            'payload': request.payload,
            'timestamp': request.timestamp
        }
        self.message_queue.put(message)
        logger.info(f"Received message with ID: {message_id} and payload: {request.payload}")
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