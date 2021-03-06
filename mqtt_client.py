import paho.mqtt.client as paho
import time
# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client


import serial
serdev = '/dev/ttyACM5'
s = serial.Serial(serdev, 9600)

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your IP
host = "172.20.10.11"
topic = "Mbed"
mode = '0'

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) +"\n")
    mode = str(msg.payload)[9]
    if(mode == '0'):                # gesture mode
        deg = str(msg.payload)[24]  # get the confirm angle
        time.sleep(1)
        s.write(bytes("/resewee/run\n", 'UTF-8'))   # reset mbed
        time.sleep(10)
        s.write(bytes("/angle/run " + deg +"\n", 'UTF-8'))  # tell mbed the confimed angle
        print("set angle OK")
    else:                           # tilt mode
        t = (int)(str(msg.payload)[12]) # get how many times over angle
        time.sleep(2)
        if(t >= 5):                 # if over five times, reset mbed    
            s.write(bytes("/resewee/run\n", 'UTF-8'))
            time.sleep(5)
            print("back to rpcloop")
    #s.close()


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")


# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)



# Loop forever, receiving messages
mqttc.loop_forever()




