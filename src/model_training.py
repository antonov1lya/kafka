import time
import json
import config

from confluent_kafka import Producer, Consumer
from datetime import datetime
from river import tree, preprocessing, metrics


def data_preparation(x):
    x['tpep_pickup_datetime'] = datetime.strptime(
        x['tpep_pickup_datetime'], "%Y-%m-%d %H:%M:%S")
    x['tpep_dropoff_datetime'] = datetime.strptime(
        x['tpep_dropoff_datetime'], "%Y-%m-%d %H:%M:%S")
    x['duration'] = int((x['tpep_dropoff_datetime'] -
                        x['tpep_pickup_datetime']).seconds/60)
    x['hour'] = x['tpep_pickup_datetime'].hour
    x.pop('tpep_pickup_datetime')
    x.pop('tpep_dropoff_datetime')
    y = x.pop('total_amount')
    return x, y


def prepare_data_for_visualizer(sample_x, metric):
    return {'duration': sample_x['duration'], 'distance': sample_x['trip_distance'],
            'metric': metric}


def model_training():
    consumer = Consumer(config.MODEL_TRAINING_CONSUMER_CONFIG)
    consumer.subscribe([config.DATA_MINER_TOPIC])

    producer = Producer(config.MODEL_TRAINING_PRODUCER_CONFIG)

    model = (
        preprocessing.StandardScaler() |
        tree.HoeffdingTreeRegressor(grace_period=100, model_selector_decay=0.9)
    )
    metric = metrics.MAPE()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            sample_x, sample_y = data_preparation(sample)
            model.learn_one(sample_x, sample_y)
            metric.update(sample_y, model.predict_one(sample_x))
            to_visualizer = prepare_data_for_visualizer(sample_x, metric.get())
            print(to_visualizer)
            producer.produce(config.MODEL_TRAINING_TOPIC, key='1',
                             value=json.dumps(to_visualizer))
            producer.flush()
            time.sleep(1)


if __name__ == "__main__":
    model_training()
