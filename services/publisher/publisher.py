import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, timezone
import random    # fake values

# Settings values for loop value gaus random generation
# Simulating vibration values for Healthy vibrations 
sigma = 0.1
mu = 0
n = 10  # number of values generated 
interval_s = 1

# Create a client
# Client -> Object that connects to broker - later steps is a method on it.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
'''Note: 
keyword "Callback" -> function written that Paho calls when something happens:
    - on_connect: the broker answered your CONNECT
    - on_message: a message arrived on a topic you subscribed to
    - on_disconnect: the connection closed
You hand them to client -> Network loop calls them at right moment.
Publisher doesn't use any yet, but subscriber will need "on_message",
in order to receive messages to the code.
   
   Note2: 
Paho went from version 1 to version 2. What changed?
    - Information that callbacks receive.
        e.g.: on_connect gets "reason code" -> why connection succeeded or not
        VERION2: current style
   
   Note3: 
mqtt - module imported
CallbackAPIVersion - fixed list of allowed options inside mqtt module (enum)
VERSION2 - option picked
'''

# Connection to localhost on port 1883
client.connect(host="localhost", port=1883)
# Does TCP connection + Sends MQTT's CONNECT

# Start network loop
client.loop_start()  
''' Paho doesn't send and receive messages over the network by itself. 
Something has to keep pushing bytes out, reading replies like CONNACK, 
and sending keep-alive pings. That's the network loop! loop_start() runs 
it in the background while the script continues. Without it, message can 
get stuck and never leave.
'''
try:
    while True: 

        timestamp = datetime.now(timezone.utc).isoformat()

        
        # List comprehension - generating a list of n values of vibrations
        values = [random.gauss(mu, sigma) for _ in range(n)]  #_ is loop variable. no need, so _

        # Generating the payload json dictionary
        payload = {"sensor_id":"bearing1",  # Identitication of data sensor id
                "timestamp": timestamp,     # When data was created
                "sample_rate_hz":12000,     # How measured: 12000 samples/sec
                "units":"g",                # Unit of the values g (not m/s^2, volts or ADC counts)
                "values":values}            # What was measured: n samples in g

        # Network can only carry text or bytes. so json dict needs to be converted
        payload_json = json.dumps(payload)

        # Publish and wait for it to go out (test)
        info = client.publish(topic="plant/line1/bearing1/vibration", payload=payload_json, qos=0)
        info.wait_for_publish()

        print(f'Published: {timestamp}')  

        time.sleep(interval_s)   # pauses script for one second
    
except KeyboardInterrupt:
    # Ends the loop, so the script can finish instead of leaving it hanging.   
    client.loop_stop()
    print("Loop Stopped")

finally: 
    # Clean Up
    # Sends MQTTs DISCONNECT message to broker, then closes TCP connection
    client.disconnect()




