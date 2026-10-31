import paho.mqtt.client as mqtt

# on_message function -> Callback, function paho calls everytime message arrives

def on_message(client, userdata, message):
    '''
    Callback that Paho runs every time a message arrives on a subscribed topic.

    I don't call this function myself: I attach it with client.on_message = on_message,
    and the network loop (loop_forever) calls it whenever the broker delivers a message.

    Args:
        client: the Paho client that received the message.
        userdata: optional data I can attach to the client; not used here.
        message: the received message. message.topic is the topic as a string;
            message.payload is the content as bytes, so it needs .decode() to become text.
    '''
    topic = message.topic     # topic as a string
    payload = message.payload.decode() # content as bytes. (to make it string -> .decode())

    print(f'{topic}: {payload}')

# Creating client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Attach function to client
client.on_message = on_message   # handing Paho function itself, for later call

# Connection to localhost on port 1883
client.connect(host="localhost", port=1883)

# Subscribe
client.subscribe(topic = "test", qos = 0)

# Run loop forever
client.loop_forever()