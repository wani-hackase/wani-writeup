import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, respons_code):
    print("connected")
    client.subscribe("$internal/admin/webcam")


def on_message(client, userdata, msg):
    print("receive message")
    f = open("webcam.jpg", "wb")
    f.write(msg.payload)
    f.close()


client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 60805, 60)
client.loop_forever()
