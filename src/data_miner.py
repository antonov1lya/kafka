import time
import json
import config

from confluent_kafka import Producer
from river import stream


def data_miner():
    producer = Producer(config.DATA_MINER_PRODUCER_CONFIG)

    dateset_size = 200000
    dataset_stream = stream.iter_csv(
        'nyc_yellow_taxi.csv',
        converters={
            'VendorID': int,
            'tpep_pickup_datetime': str,
            'tpep_dropoff_datetime': str,
            'passenger_count': int,
            'trip_distance': float,
            'RateCodeID': int,
            'total_amount': float
        }
    )

    for _ in range(dateset_size):
        sample_x, sample_y = next(dataset_stream)
        producer.produce(config.DATA_MINER_TOPIC, key='1',
                         value=json.dumps(sample_x))
        producer.flush()
        print(sample_x)
        time.sleep(1)


if __name__ == "__main__":
    data_miner()
