import paho.mqtt.client as mqtt

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
''' Paho doesn't send and recieve messages over the network by itself. 
Something has to keep pushing bytes out, reading replies like CONNACK, 
and sending keep-alive pings. That's the network loop! loop_start() runs 
it in the background while the script continues. Without it, message can 
get stuck and never leave.
'''

# Publish and wait for it to go out (test)
info = client.publish(topic="test", payload="hello from Python", qos=0)
info.wait_for_publish()

# Clean Up
# Sends MQTTs DISCONNECT message to broker, then closes TCP connection
client.disconnect()
# Ends the loop, so the script can finish instead of leaving it hanging.   
client.loop_stop()
