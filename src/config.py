DATA_MINER_TOPIC = 'data_producer'
DATA_MINER_PRODUCER_CONFIG = {'bootstrap.servers': 'localhost:9095'}

MODEL_TRAINING_TOPIC = 'model_results'
MODEL_TRAINING_CONSUMER_CONFIG = {
    'bootstrap.servers': 'localhost:9095', 'group.id': 'model_training'}
MODEL_TRAINING_PRODUCER_CONFIG = {'bootstrap.servers': 'localhost:9095'}

VISUALIZER_CONSUMER_CONFIG = {
    'bootstrap.servers': 'localhost:9095', 'group.id': 'visualizer'}
