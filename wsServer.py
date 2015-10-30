#!/usr/bin/python
####################################################
# Name: Donation Box WebSockets deamon 
#
# Description:
# Provides the WebSockets Server which polls data from the DB, notifies any connected clients (browsers)
# and accepts messages (donations) from clients that then writes to the DB
#
# Author: Dimitris Koukoulakis
#
# License: GNU GPL v3.0
####################################################

from __future__ import print_function
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
import json
import logging
from time import gmtime, strftime
from Adafruit_Thermal import *


#Init
json_data=open('config.json')
config = json.load(json_data)
json_data.close()
logging.basicConfig(filename='wsServer.log', level=logging.DEBUG, format='%(levelname)s %(asctime)s: %(message)s')
logging.debug('wsServer started')

coin = 0
#See the config.json file for the configuration
curr = config["General"]["currency"]
init_wait_time = config["General"]["Init Wait time (sec)"]
clients = []
dbserver = config["Database"]["server"]
dbuser = config["Database"]["username"]
dbpass = config["Database"]["password"]
dbname = config["Database"]["name"]

pr_enabled = config["Printer"]["enabled"]
pr_dev = config["Printer"]["dev"]
pr_baudrate = config["Printer"]["baudrate"]
pr_timeout = config["Printer"]["timeout"]
pr_feedlines = config["Printer"]["feedlines"]
pr_heattime = config["Printer"]["heattime"]

#wait at start up for mySQL to load
time.sleep(init_wait_time)

if pr_enabled:
  printer = Adafruit_Thermal(pr_dev, pr_baudrate, timeout=pr_timeout)

def Th_print(currency,value,name,email,prname,prid,donationid):
  if not pr_enabled:
    logging.debug('Thermal printer is disabled')
    return
    
  printer.begin(pr_heattime) 
  printer.setTimes(0,0) #print as fast as possible
  logging.debug('Printing donation to thermal printer')  
  printer.boldOn()
  printer.println('THANK YOU')
  printer.println(name)
  printer.boldOff()
  printer.print(value)
  printer.print(currency)
  printer.print(' to ')
  printer.print(prname)
  printer.println(' project')
  printer.println('Your donation registered')
  if email != '':
    printer.print('with ')
    printer.print(email)
     
  printer.feed(pr_feedlines)

  
def QueryDBonStart():	
  global dbserver
  global dbname
  global dbuser
  global dbpass
  global coin
  global curr

  #Connect to Database
  dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")
  cursor = dbConn.cursor()

  try:
    #print "Query DB...";
    #See if there are coins inserted that have not been donated
    sql = "SELECT currency,value,donationid FROM coinacceptor WHERE donationid < 0";
    cursor.execute(sql);
    # Get returned values
    for (currency,value,donationid) in cursor:
      #TODO: What should happen if one coin is of differenct currency?
      curr = currency
      coin += value
      logging.debug('DonationID: '+repr(donationid)+' Currency: '+repr(curr)+' Value: '+repr(coin))

    if coin != 0:
      # Send value and currency to web socket client
      send_donation(coin,curr)        
    cursor.close();  #close the cursor
  except MySQLdb.IntegrityError:
    logging.error('failed to fetch data')
  finally:
    cursor.close()  #close just incase it failed
  
  
def send_donation(c, msg):
  logging.debug('SEND: %s %s',str(c),msg)
  for client in clients:
    client.write_message(str(c)+msg)
  global coin
  global curr
  coin = 0
  curr = "EUR"


def send_project_total(pid, msg):
  logging.debug('PID|'+str(pid)+'|TOTAL|'+msg)
  for client in clients:
    client.write_message("PID|"+str(pid)+"|TOTAL|"+msg)


def QueryDB():
  LastTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  while True:
    dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")
    cursor = dbConn.cursor()

    try:
      #print "Query DB...";
      sql = "SELECT timeinserted, value, currency FROM coinacceptor WHERE timeinserted > %s ORDER BY timeinserted DESC";
      #logging.debug('RUN SQL: SELECT timeinserted, value, currency FROM coinacceptor WHERE timeinserted > %s ORDER BY timeinserted DESC', LastTime)
      cursor.execute(sql,LastTime);

      data = cursor.fetchone();
      for (timeinserted, value, currency) in cursor:
        LastTime = timeinserted
        global coin
        coin = value
        global curr
        curr = currency
        logging.debug('%d %s', coin, curr)
        if coin != 0:
          send_donation(coin,curr)
      #print data
      cursor.close();  #close the cursor
    except MySQLdb.IntegrityError:
      logging.error('failed to fetch data')
    finally:
      cursor.close()  #close just incase it failed
    time.sleep(0.5);
    
    
def InsertDonation(currency,value,name,email,public, prname, prid):
  from time import gmtime, strftime
  timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")
  logging.debug('Insert donation to DB')
  dbConn.set_character_set('utf8')
  
  cursor = dbConn.cursor()
  
  cursor.execute('SET NAMES utf8;')
  cursor.execute('SET CHARACTER SET utf8;')
  cursor.execute('SET character_set_connection=utf8;')
  
  logging.debug('Name:'+name+' Email:'+email+' public:'+public+' Project Name:'+prname+' ProjectID:'+prid+' Currency:'+currency+' Value:'+value)
  if (public == 'false'):
    public = 0
  else:
    public = 1
  try:
    #Insert donation
    sql = "INSERT INTO donations (currency,ammount,projectname,email,name,public,projectid,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(currency,value,prname,email,name,public,prid,timestamp))
    dbConn.commit()
    #Get donation ID
    donationid = cursor.lastrowid
    #Update coins inserted with donation ID
    sql = "UPDATE coinacceptor SET donationid=%s WHERE donationid=-1"
    logging.debug('RUN SQL: UPDATE coinacceptor SET donationid=%s WHERE donationid=-1', donationid)
    cursor.execute(sql,donationid)
    dbConn.commit()
    cursor.close()
  except MySQLdb.IntegrityError:
    logging.error('failed to fetch data')
    for client in clients:
      client.write_message("ERROR")
  finally:
    cursor.close()  #close just incase it failed
    for client in clients:
      client.write_message("SUCCESS")
      logging.info('Data written successfuly')
  return donationid;  
    
def GetProjectTotal(pid):
  dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")

  cursor = dbConn.cursor()
  value = 0
  
  try:
    sql = "SELECT SUM(Ammount) FROM donations WHERE ProjectID = %s";
    logging.debug('RUN SQL: SELECT SUM(Ammount) FROM donations WHERE ProjectID = %s', pid)
    cursor.execute(sql,pid);
    data = cursor.fetchone();
    for (amount) in cursor:
      value = amount

    cursor.close();  #close the cursor
    logging.debug('Get project total amount donated: %d', value)
    return value    
  except MySQLdb.IntegrityError:
    logging.error('failed to fetch data')
  finally:
    cursor.close()


def processdonation(msg):
  logging.debug('Process donation: %s', msg)
  values = msg.split('|')
  name = values[0]
  email = values[1]
  public = values[2]
  prname = values[3]
  projectdetails = values[4].split('?') #contains language info (e.g. 81?lang=el)
  prid = projectdetails[0]
  lang = projectdetails[1]  #lang support for printer limited to ASCII
  dondata = values[5]
  l = len(dondata)
  donvalue = dondata[0:l-3]
  doncurr = dondata[l-3:]
  #print donvalue
  #print doncurr
  donationid = InsertDonation(doncurr,donvalue,name,email,public,prname,prid)
  Th_print(doncurr,donvalue,name,email,prname,prid,donationid)

def processmsg(msg):
  logging.debug('Process message: %s', msg)
  values = msg.split('|')
  if (values[0] == 'REQPROJECTTOTAL'):
    s = GetProjectTotal(values[1])
    send_project_total(values[1],s)
  else:
    processdonation(msg)
 

class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self):
    logging.info('New connection was opened')
    clients.append(self)
    QueryDBonStart()
 
  def on_message(self, message):
    processmsg(message)
 
  def on_close(self):
    logging.info('Connection was closed...')
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
