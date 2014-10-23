#!/usr/bin/python
####################################################
# Name: Donation Box Web Socket Server
#
# Description:
# Reads a DB table for new entries. If a new entry is found it sends the Currency and Value to the Web Socket Client
#
# Author: Dimitris Koukoulakis
#
# License: GNU GPL v3.0
####################################################

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import serial 
import MySQLdb 
import time
import threading
import datetime
import decimal

coin = 0;
curr = "EUR";
clients = []


def send_donation(c, msg):
  for client in clients:
    client.write_message(str(c)+msg)
  global coin
  global curr
  coin = 0
  curr = "EUR"


def QueryDB():
  from time import gmtime, strftime
  LastTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  while True:
    dbConn = MySQLdb.connect("localhost","root","c0mm0ns","wordpress") or die ("could not connect to database")
    cursor = dbConn.cursor()

    try:
      print "Query DB...";
      sql = "SELECT timeinserted, value, currency FROM coinacceptor WHERE timeinserted > %s ORDER BY timeinserted DESC";
      cursor.execute(sql,LastTime);

      data = cursor.fetchone();
      for (timeinserted, value, currency) in cursor:
        LastTime = timeinserted
        global coin
        coin = value
        global curr
        curr = currency
        print LastTime
        print coin
        print curr
        if coin != 0:
          send_donation(coin,curr)
      print data

      cursor.close();  #close the cursor
    except MySQLdb.IntegrityError:
      print "failed to fetch data"
    finally:
      cursor.close()  #close just incase it failed
    time.sleep(0.5);

class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self):
    print 'New connection was opened'
    clients.append(self)
    self.write_message("Welcome to my websocket!")
 
  def on_message(self, message):
    print 'Incoming message:', message
    self.write_message("You said: " + message)
 
  def on_close(self):
    print 'Connection was closed...'
    clients.remove(self)

  t = threading.Thread(target=QueryDB)
  t.daemon = True
  t.start()

application = tornado.web.Application([
  (r'/ws', WSHandler),
])


if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
