#      time:       2018-3-17
#      author:     songshu
#      function:   using mqtt technology
#                  send command and file to the device controled
#                  on the device part
#       version:    Python: 2.7.3
#                   paho-mqtt: 1.1

import paho.mqtt.client as mqtt
import json
import time
import mraa

led = []
time_end = 0
Error_str = "Error order!"
NAME = 'device_1'
HOST = "iot.eclipse.org"
# HOST = '111.231.222.203'
PORT = 1883

# deal with the command from control
def deal_cmd(client, cmd):
    if cmd[0:-2] == "turn on led":
        index = cmd[-1]
        if index >= '0' and index <= '9':
            led[int(index)].write(1)
        else:
            client.publish("ack_message", json.dumps({"user": NAME, "say": Error_str}))
        print("led " + index + " is on")
    if cmd[0:-2] == "turn off led":
        index = cmd[-1]
        if index >= '0' and index <= '9':
            led[int(index)].write(0)
        else:
            client.publish("ack_message", json.dumps({"user": NAME, "say": Error_str}))
        print("led " + index + " is off")
    client.publish('ack_message', json.dumps({'user':NAME, 'message':'I have got the command!'}), qos=0)

# dela with the file data, and save it
def deal_file(client, file_name, data):
    with open('down/'+ file_name, 'w') as file:
        file.write(data)
    client.publish('ack_message', json.dumps({'user':NAME, 'message':'the cmd have beed done!'}), qos=0)

# deal with the cook
def deal_cook(client, message):
    global time_end
    msg = message.split(':')
    if msg[0] == 'egg':
        time_end = time.time() + int(msg[1])*60
        led[0].write(1)
        client.publish('ack_message', json.dumps({'user':NAME, 'message':'the cmd have been done!\ncook start'}), qos=0)
        print('cook start')

# connect function , do it just when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # subscribe the title used, control_message and ack_message
    print('Connected with result code '+str(rc))
    client.subscribe('control_message', qos=0)
    client.publish('ack_message', json.dumps({'user': NAME , 'message': 'hello, I am here'}), qos=0)

# message function, do it just when broker have got the message
def on_message(client, userdatga, msg):
    payload = json.loads(msg.payload.decode())
    user = payload.get('user')
    message = payload.get('message')
    # data split to get the control_name, class and file_name
    # print(user +':' + message)
    user = user.split(':')
    # data error, it will happen when the first connect to the broker
    if len(user) == 1:
        return
    # get the cmd data
    if user[1] == 'cmd':
        deal_cmd(client, message)
        print('cmd')
    # get the file data
    if user[1] == 'file':
        deal_file(client, user[2], message)
        # print('file'+'qos:', msg.qos)
    if user[1] == 'cook':
        deal_cook(client, message)

def led_init():
    for x in [31, 32, 33, 35, 36, 37, 38, 40]:
        led.append(mraa.Gpio(x))
    for x in led:
        x.dir(mraa.DIR_OUT)
        x.write(0)

def main():
    global time_end
    led_init()
# initialize the mqtt client
    client = mqtt.Client()
    client.username_pw_set('admin', 'password')
    client.on_connect = on_connect
    client.on_message = on_message
# connect the mqtt broker
    client.connect(HOST, PORT, 60)
# set the user name
    client.user_data_set(NAME)
# client start
    client.loop_start()
# system loop for getting command and file
    while True:
        if (time_end < time.time()) and (time_end != 0):
            time_end = 0
            led[0].write(0)
            client.publish('ack_message', json.dumps({'user':NAME,'message':'cook stop!'}), qos=0)
            print('cook stop')
        led[7].write(1)
        time.sleep(1)
        led[7].write(0)
        time.sleep(1)

if __name__ == '__main__':
    main()