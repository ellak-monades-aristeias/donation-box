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

json_data=open('/home/pi/donation-box/config.json')
config = json.load(json_data)
json_data.close()

#wait at start up for mySQL to load
time.sleep(60)

coin = 0
#See the config.json file for the configuration
curr = config["General"]["currency"]
clients = []
dbserver = config["Database"]["server"]
dbuser = config["Database"]["username"]
dbpass = config["Database"]["password"]
dbname = config["Database"]["name"]

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
      print 'DonationID: '+repr(donationid)+' Currency: '+repr(curr)+' Value: '+repr(coin)

    if coin != 0:
      # Send value and currency to web socket client
      send_donation(coin,curr)        
    cursor.close();  #close the cursor
  except MySQLdb.IntegrityError:
    print "failed to fetch data"
  finally:
    cursor.close()  #close just incase it failed
  
  
def send_donation(c, msg):
  for client in clients:
    client.write_message(str(c)+msg)
  global coin
  global curr
  coin = 0
  curr = "EUR"


def send_project_total(pid, msg):
  print "PID|"+str(pid)+"|TOTAL|"+msg
  for client in clients:
    client.write_message("PID|"+str(pid)+"|TOTAL|"+msg)


def QueryDB():
  from time import gmtime, strftime
  LastTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  while True:
    dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")
    cursor = dbConn.cursor()

    try:
      #print "Query DB...";
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
      #print data
      cursor.close();  #close the cursor
    except MySQLdb.IntegrityError:
      print "failed to fetch data"
    finally:
      cursor.close()  #close just incase it failed
    time.sleep(0.5);
    
    
def InsertDonation(currency,value,name,email,public, prname, prid):
  from time import gmtime, strftime
  timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime());
  dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")
  
  dbConn.set_character_set('utf8')
  
  cursor = dbConn.cursor()
  
  cursor.execute('SET NAMES utf8;')
  cursor.execute('SET CHARACTER SET utf8;')
  cursor.execute('SET character_set_connection=utf8;')
  
  print 'Name:'+name+' Email:'+email+' public:'+public+' Project Name:'+prname+' ProjectID:'+prid+' Currency:'+currency+' Value:'+value
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
    cursor.execute(sql,donationid)
    dbConn.commit()
    cursor.close()
  except MySQLdb.IntegrityError:
    print "failed to fetch data"
    for client in clients:
      client.write_message("ERROR")
  finally:
    cursor.close()  #close just incase it failed
    for client in clients:
      client.write_message("SUCCESS")
    
    
def GetProjectTotal(pid):
  dbConn = MySQLdb.connect(dbserver,dbuser,dbpass,dbname) or die ("could not connect to database")

  cursor = dbConn.cursor()
  value = 0
  
  try:
    sql = "SELECT SUM(Ammount) FROM donations WHERE ProjectID = %s";
    cursor.execute(sql,pid);
    data = cursor.fetchone();
    for (amount) in cursor:
      value = amount

    cursor.close();  #close the cursor
    return value    
  except MySQLdb.IntegrityError:
    print "failed to fetch data"
  finally:
    cursor.close()


def processdonation(msg):
  print msg
  values = msg.split('|')
  name = values[0]
  email = values[1]
  public = values[2]
  prname = values[3]
  prid = values[4]
  dondata = values[5]
  l = len(dondata)
  donvalue = dondata[0:l-3]
  doncurr = dondata[l-3:]
  #print donvalue
  #print doncurr
  InsertDonation(doncurr,donvalue,name,email,public,prname,prid)


def processmsg(msg):
  values = msg.split('|')
  print msg
  if (values[0] == 'REQPROJECTTOTAL'):
    s = GetProjectTotal(values[1])
    send_project_total(values[1],s)
  else:
    processdonation(msg)
 

class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self):
    print 'New connection was opened'
    clients.append(self)
    QueryDBonStart()
 
  def on_message(self, message):
    processmsg(message)
 
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
