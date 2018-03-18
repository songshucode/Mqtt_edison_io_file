#      time:       2018-3-17
#      author:     songshu
#      function:   using mqtt technology
#                  send command and file to the device controled
#                  on the device part

import paho.mqtt.client as mqtt
import json
import time

NAME = 'device_1'
HOST = '111.231.222.203'
PORT = 1883

# deal with the command from control
def deal_cmd(client, cmd):
    client.publish('ack_message', json.dumps({'user':NAME, 'message':'I have got the command!'}), qos=2)

# dela with the file data, and save it
def deal_file(client, file_name, data):
    with open('down/'+ file_name, 'w') as file:
        file.write(data)
    client.publish('ack_message', json.dumps({'user':NAME, 'message':'the cmd have beed done!'}), qos=2)

# connect function , do it just when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # subscribe the title used, control_message and ack_message
    print('Connected with result code '+str(rc))
    client.subscribe('control_message', qos=2)
    client.publish('ack_message', json.dumps({'user': NAME , 'message': 'hello, I am here'}), qos = 2)

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
        print('file'+'qos:', msg.qos)

def main():
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
        time.sleep(10)

if __name__ == '__main__':
    main()