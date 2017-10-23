import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tornado
import tornado.websocket
import time
import datetime
import json
import ast
import Queue

qmsg = Queue.Queue()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    tt = datetime.datetime.now()
    def check_origin(self, origin):
        #print "origin: " + origin
        return True
    # the client connected
    def open(self):
        print ("New client connected")
        self.write_message("You are connected")
        clients.append(self)
        tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), self.test)

    def test(self):
        try:
            info = {}
            try:
                text = qmsg.get()
                print("TEXT: ")
                print(text)
                values = str(text).split(".")
                """
		info = {
                    "luz"      : float(values[1]),
                    "humedad"  : float(values[2]),
                    "temperatura"   : float(values[3]),
                    "tierra" : float(values[0]),
                    "estado"    : int(values[3]),
                    "timestamp" : time.time()
		}
		"""
                info = {
                    "luz"      : float(values[0]), 
                    "humedad"  : float(values[1]), 
                    "temperatura"   : float(values[2]), 
                    #"tierra" : float(values[0]), 
                    "estado"    : int(values[3]),
                    "timestamp" : time.time()
                }
                print info
            except Exception as e:
                print("EXCEPTION IN TEST READ FROM READ SERIAL: ")
                print(e)
                #print(info)
                info = {
                    "humedad"  : float("0.0"),
                    "temperatura"   : float("0.0"),
                    "tierra" : float("0.0"),
                    "estado"    : -1,
                    "timestamp" : time.time()
                }
                #raise(e)
            print(info)
            self.write_message(info)
        except Exception as e:
            print ("restartplease")
            self.write_message("restartplease")
            print e
            #raise(e)
        else:
            tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=0.1), self.test)


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
   list = json.loads(msg.payload)
   data_json = {}
   for key,value in list.iteritems():
       data_json[key] = value
       print ("")
       print key, value
       print "data_json"
       print data_json
       qmsg.put(data_json)

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
    mqtt.client.loop_forever()
    socket = tornado.web.Application([(r"/websocket", WebSocketHandler),])
    print("Opening port 8888")
    socket.listen(8888)
