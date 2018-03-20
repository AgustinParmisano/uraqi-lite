import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tornado
import tornado.websocket
import time
import datetime
from datetime import timedelta
import json
import ast
import Queue

qmsg = Queue.Queue()
clients = []

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    tt = datetime.datetime.now()
    def check_origin(self, origin):
        #print "origin: " + origin
        return True
    # the client connected
    def open(self):
        print ("New client connected")
        clients.append(self)
        tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), self.test)

    def test(self):
        try:
            message = str(qmsg.get())
            message = ast.literal_eval(json.dumps(message))
            message = ast.literal_eval(message)

            try:
                time.sleep(1)
                self.write_message(message)
            except Exception as e:
                print "Exception in test write message: "
                print e
                raise(e)
        except Exception as e:
            print "Exception in test write message 2: "
            print e
            raise(e)
        else:
            tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=0.1), self.test)

    def on_message(self, message):
        try:
           msg = json.loads(message.payload)
           data_json = {}
        except Exception as e:
          print "Exception in websocket class on_message: "
          print e

def msg_ws(msg):
   resp = publish.single("data_to_web", msg, hostname="localhost")
   return resp


def on_connect(client, userdata, flags, rc):
   print("MQTT Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   #client.subscribe("sensors/new_sensor")
   client.subscribe("sensors/new_data")


data_list = []

def on_message(client, userdata, msg):
   print("msg.topic: " + msg.topic+" msg.payload "+str(msg.payload))
   payload = str(msg.payload)
   data_dict = ast.literal_eval(payload)
   qmsg.put(data_dict)

def on_subscribe(client, userdata,mid, granted_qos):
   print "userdata : " +str(userdata)

def on_publish(mosq, obj, mid):
   print("mid: " + str(mid))

class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost", 1883, 60)
        actions = Queue.Queue()

    def get_actions_queue(self):
        return self.actions

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(message, topic):
         print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %d " % (message)

socket = tornado.web.Application([(r"/websocket", WebSocketHandler),])
if __name__ == "__main__":
    print "Starting MQTT"
    mqtt = MqttClient()
    mqtt.client.loop_start()
    socket = tornado.web.Application([(r"/websocket", WebSocketHandler),])
    print("Opening port 8888")
    socket.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
tornado.ioloop.IOLoop.instance().start()
