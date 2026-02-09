"""
Kafka service for publishing and consuming messages
"""
import json
import logging
from typing import Optional
from confluent_kafka import Producer, Consumer, KafkaError
from app.core.config import settings

logger = logging.getLogger(__name__)


class KafkaService:
    """Service to handle Kafka pub/sub operations"""
    
    def __init__(self):
        """Initialize Kafka service with producer and consumer configs"""
        self.producer_config = {
            'bootstrap.servers': settings.KAFKA_BROKER,
            'client.id': 'todo-producer',
            'message.timeout.ms': 2000,  # 2 second timeout for messages
            'socket.timeout.ms': 2000    # 2 second socket timeout
        }
        self.consumer_config = {
            'bootstrap.servers': settings.KAFKA_BROKER,
            'group.id': 'todo-consumer-group',
            'auto.offset.reset': 'earliest'
        }
        self.topic = settings.KAFKA_TOPIC
        self.producer = None
        self.consumer = None
    
    def publish_message(self, message: dict) -> bool:
        """
        Publish a message to Kafka topic
        
        Args:
            message: Dictionary containing message data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.producer:
                self.producer = Producer(self.producer_config)
            
            # Convert message to JSON
            message_json = json.dumps(message)
            
            # Publish to Kafka (non-blocking)
            self.producer.produce(
                self.topic,
                key=str(message.get('id', 'unknown')).encode('utf-8'),
                value=message_json.encode('utf-8'),
                callback=self._delivery_report
            )
            
            # Poll to trigger delivery callbacks without blocking
            self.producer.poll(0)
            logger.info(f"Message queued for publishing to {self.topic}: {message}")
            return True
        
        except Exception as e:
            logger.error(f"Error publishing message to Kafka: {e}")
            return False
    
    def _delivery_report(self, err, msg):
        """
        Delivery report callback for Kafka producer
        
        Args:
            err: Error object if message delivery failed
            msg: Message object
        """
        if err is not None:
            # Only log as debug to avoid noise when Kafka is unavailable
            logger.debug(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    
    def start_consumer(self):
        """Start consuming messages from Kafka topic"""
        try:
            self.consumer = Consumer(self.consumer_config)
            self.consumer.subscribe([self.topic])
            logger.info(f"Consumer started for topic: {self.topic}")
        except Exception as e:
            logger.error(f"Error starting consumer: {e}")
    
    def consume_message(self, timeout: float = 1.0) -> Optional[dict]:
        """
        Consume a single message from Kafka
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Parsed message dict or None if no message available
        """
        try:
            if not self.consumer:
                self.start_consumer()
            
            msg = self.consumer.poll(timeout)
            
            if msg is None:
                return None
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    return None
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    return None
            
            # Parse and log the message
            message_value = msg.value().decode('utf-8')
            message_data = json.loads(message_value)
            logger.info(f"Message consumed from {msg.topic()}: {message_data}")
            return message_data
        
        except Exception as e:
            logger.error(f"Error consuming message: {e}")
            return None
    
    def close(self):
        """Close producer and consumer connections"""
        try:
            if self.producer:
                # Use a short timeout to avoid hanging if Kafka is unavailable
                self.producer.flush(timeout=1)
                self.producer = None
            if self.consumer:
                self.consumer.close()
                self.consumer = None
            logger.info("Kafka connections closed")
        except Exception as e:
            logger.debug(f"Error closing Kafka connections: {e}")


# Create a singleton instance
kafka_service = KafkaService()
