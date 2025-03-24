
import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker Details
BROKER = "mqtt.eclipseprojects.io"  # Public MQTT broker
TOPIC = "veriharvest/sensor"

# Simulated Sensor Data Function
def generate_sensor_data():
    return {
        "temperature": random.uniform(2, 10),  # Simulating temperature values (°C)
        "humidity": random.uniform(40, 70),  # Simulating humidity values (%)
        "gas_level": random.uniform(0.1, 2.0)  # Simulated gas contamination levels (PPM)
    }

# MQTT Client Setup
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")

def publish_sensor_data():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, 1883, 60)
    
    while True:
        sensor_data = generate_sensor_data()
        client.publish(TOPIC, str(sensor_data))
        print(f"Published: {sensor_data}")
        time.sleep(5)  # Sends data every 5 seconds

if __name__ == "__main__":
    publish_sensor_data()
