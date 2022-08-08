import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
from src.models import FlowRate

from sqlalchemy import create_engine, insert
from datetime import datetime, time

SQLALCHEMY_DATABASE_URL = os.environ['irrigation_conn_string']
IOT_CORE_EP = os.environ['IOT_CORE_EP']
DEVICE = os.environ['DEVICE']
TOPIC = os.environ['TOPIC']

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def insert_flow_rate(data):
    with engine.connect() as conn:
        data['flow_timestamp'] = datetime.combine(
            datetime.today(),
            time(hour=data['flow_hour'], minute=data['flow_minute'], second=data['flow_second'])
        )
        result = conn.execute(insert(FlowRate), [data])


def customCallback(client,userdata,message):
    data = json.loads(message.payload)
    insert_flow_rate(data)


base_path = os.getcwd()
myMQTTClient = AWSIoTMQTTClient(DEVICE)
myMQTTClient.configureEndpoint(IOT_CORE_EP, 8883)
myMQTTClient.configureCredentials(
    os.path.join(base_path, "src/iot_core/devices/flow-rate-dumper/AmazonRootCA1.pem"),
    os.path.join(base_path, "src/iot_core/devices/flow-rate-dumper/key-private.pem.key"),
    os.path.join(base_path, "src/iot_core/devices/flow-rate-dumper/device-certificate.pem.crt")
)

myMQTTClient.connect()
print("Client Connected")

myMQTTClient.subscribe(TOPIC, 1, customCallback)
print('waiting for the callback. Click to conntinue...')
x = input()

myMQTTClient.unsubscribe(TOPIC)
print("Client unsubscribed")

myMQTTClient.disconnect()
print("Client Disconnected")
