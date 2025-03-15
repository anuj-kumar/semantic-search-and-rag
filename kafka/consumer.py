from confluent_kafka import Consumer, KafkaException
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

def consume_messages(consumer_config, sr_conf, topics, listener, converter):
    schema_registry_client = SchemaRegistryClient(sr_conf)

    avro_deserializer = AvroDeserializer(schema_registry_client, None, converter)


    consumer = Consumer(consumer_config)
    consumer.subscribe(topics)

    try:
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                event = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                listener(event)
                consumer.commit(msg)

            except SerializerError as e:
                print(f"Message deserialization failed: {e}")
                continue

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
