import json
import config

from confluent_kafka import Consumer
import streamlit as st
import matplotlib.pyplot as plt

features = ['duration', 'distance', 'metric']


def create_session_states():
    for feature in features:
        if feature not in st.session_state:
            st.session_state[feature] = []


def add_values_to_session_state(sample):
    for feature in features:
        st.session_state[feature].append(sample[feature])


def draw_mape_dashboard(mape):
    mape.line_chart(st.session_state['metric'],
                    x_label='dataset size', y_label='mean absolute percentage error')


def draw_duration_dashboard(duration):
    fig, ax = plt.subplots()
    ax.hist(st.session_state['duration'], bins=20)
    ax.set_xlabel('duration (minutes)')
    ax.set_ylabel('count')
    duration.pyplot(fig)
    plt.close()


def draw_correlation_dashboard(correlation):
    fig, ax = plt.subplots()
    ax.scatter(st.session_state['duration'], st.session_state['distance'])
    ax.set_xlabel('duration (minutes)')
    ax.set_ylabel('distance (miles)')
    correlation.pyplot(fig)
    plt.close()


def visualizer():
    create_session_states()

    consumer = Consumer(config.VISUALIZER_CONSUMER_CONFIG)
    consumer.subscribe([config.MODEL_TRAINING_TOPIC])

    mape = st.container(border=True)
    mape.title('MAPE dependence on dataset size for HoeffdingTreeRegressor model')
    mape = mape.empty()

    duration = st.container(border=True)
    duration.title('duration distribution')
    duration = duration.empty()

    correlation = st.container(border=True)
    correlation.title('correlation between duration and distance')
    correlation = correlation.empty()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            print(sample)
            add_values_to_session_state(sample)
            draw_mape_dashboard(mape)
            draw_duration_dashboard(duration)
            draw_correlation_dashboard(correlation)


if __name__ == "__main__":
    visualizer()
