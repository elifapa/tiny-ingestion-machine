from concurrent import futures
from dataclasses import dataclass
import structlog
from stream_ingest.config import configure_logging
import grpc
import stream_ingest.ingestion_pb2_grpc as ingestion_pb2_grpc
import stream_ingest.ingestion_pb2 as ingestion_pb2
from datetime import datetime
import queue
import uuid
from dataclasses import dataclass, field
from typing import Dict, List
from queue import Queue

# Offset is stored per partition per consumer group
# topic --> N partition --> spread across broker --> every partition has a broker leader
configure_logging()
logger = structlog.get_logger()

@dataclass
class Topic:
    """Represents a Topic with message queue(s) and metadata."""
    name: str
    partition_count: int
    replication_factor: int
    created_at: datetime = field(default_factory=datetime.now)
    partitions: List[Queue] = field(default_factory=list)

    def __post_init__(self):
        self.partitions = [queue.Queue() for _ in range(self.partition_count)]

    def get_partition(self, partition_index: int) -> Queue:
        """Get the partition queue"""
        # partition_index = hash(key) % self.partition_count
        return self.partitions[partition_index]
    
class Broker(ingestion_pb2_grpc.BrokerServicer):

    def __init__(self):
        self.message_queue = queue.Queue()
        self.topics:Dict[str, Topic]  = {}

    def PullMessage(self, request, context):

        #####################################################
        ## TOPIC IMPLEMENTATION
        #####################################################
        topic_name = request.topic_name

        # Check if topic exists
        if topic_name not in self.topics:
            logger.error(f"Topic '{topic_name}' does not exist")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Topic '{topic_name}' does not exist")
            return
        
        # Pull messages from the queue in order
        topic = self.topics[topic_name]
        partition_index = 0
        pulled = 0
        while pulled < request.number_of_messages:
            partition_queue = topic.get_partition(partition_index)
            try:
                message = partition_queue.get(timeout=1)
                logger.info(f"Sent message with topic: {message['topic_name']} and partition ID: {message['partition_id']}",
                            id=message['id'], payload=message['payload'])

                response = ingestion_pb2.PullResponse(
                    topic_name=message['topic_name'],
                    id=message['id'],
                    payload=message['payload'],
                    timestamp=message['timestamp']
                )
                yield response
                pulled += 1
            
            except queue.Empty:
                logger.warning(f"Queue is empty, requested {request.number_of_messages} but only {pulled} messages available")
                break
            
            partition_index = (partition_index + 1) % topic.partition_count


    def PushMessage(self, request, context):

        #####################################################
        ## TOPIC IMPLEMENTATION
        #####################################################
        topic_name = request.topic_name
        partition_id = request.partition_id
        
        # Check if topic exists
        if topic_name not in self.topics:
            logger.error(f"Topic '{topic_name}' does not exist")
            return ingestion_pb2.PushResponse(
                success=False,
                message=f"Topic '{topic_name}' does not exist"
            )
        
        topic = self.topics[topic_name]
        
        # Validate partition_id
        if partition_id < 0 or partition_id >= topic.partition_count:
            logger.error(f"Invalid partition_id {partition_id} for topic '{topic_name}'")
            return ingestion_pb2.PushResponse(
                success=False,
                message=f"Invalid partition_id {partition_id}. Topic has {topic.partition_count} partitions (0-{topic.partition_count-1})"
            )
        #####################################################
        # Store the message in the queue with a generated UUID
        message_id = str(uuid.uuid4())
        message = {
            'id': message_id,
            'topic_name': topic_name,
            'partition_id': partition_id,
            'payload': request.payload,
            'timestamp': request.timestamp
        }
        partition_queue = topic.get_partition(partition_id)
        partition_queue.put(message)
        
        logger.info(f"Message pushed to topic '{topic_name}', partition {partition_id}",
                    id=message_id, 
                    payload=request.payload)
        
        return ingestion_pb2.PushResponse(
            success=True,
            message=f"Message pushed successfully to topic '{topic_name}', partition {partition_id}"
        )

    def AddTopic(self, request, context):
        topic_name = request.topic_name
        logger.info(f"Adding topic with name: {topic_name}")

        # topic already exists?
        if topic_name in self.topics.keys():
            logger.warning(f"Topic '{topic_name}' already exists")
            response = ingestion_pb2.AddTopicResponse(
                success=False,
                message=f"Topic '{topic_name}' already exists"
            )
            return response
        
        topic_metadata = {
            'name': request.topic_name,
            'partition_count': request.partition_count,
            'replication_factor': request.replication_factor,
            'created_at': datetime.now()
        }
        try:
            self.topics[topic_name] = Topic(**topic_metadata)
            logger.info(f"Topic '{topic_name}' added successfully")
        except Exception as e:
            logger.error(f"Failed to add topic '{topic_name}': {e}")
            response = ingestion_pb2.AddTopicResponse(
                success=False,
                message=f"Failed to add topic '{topic_name}': {e}"
            )
            return response

        response = ingestion_pb2.AddTopicResponse(
            success=True,
            message=f"Topic '{topic_name}' added successfully"
        )
        return response
    
    def ListTopics(self, request, context):
        # List all topics
        topics = []
        for topic_name, topic in self.topics.items():
            topics.append(
                ingestion_pb2.Topic(
                    name=topic.name,
                    partition_count=topic.partition_count,
                    replication_factor=topic.replication_factor,
                    created_at=int(topic.created_at.timestamp())
                )
            )
        logger.info(f"Listing {len(topics)} topics")
        response = ingestion_pb2.ListTopicsResponse(topics=topics)
        return response

def serve():
    port = "50051"
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    ingestion_pb2_grpc.add_BrokerServicer_to_server(Broker(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logger.info("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()