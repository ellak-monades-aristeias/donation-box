#!/usr/bin/python
####################################################
# Name: Donation Box Serial deamon 
#
# Description:
# Listens to serial port and writes to a DB table the currency and value received
#
# Author: Dimitris Koukoulakis
#
# License: GNU GPL v3.0
####################################################

import threading
import time
import serial 
import MySQLdb
import json
import logging

logging.basicConfig(filename='Serial2DB.log', level=logging.DEBUG, format='%(levelname)s %(asctime)s: %(message)s')
logging.debug('Serial2DB started')
json_data=open('/home/pi/donation-box/config.json')
config = json.load(json_data)
json_data.close()

last_received = ''

def WriteToDB(curr, value):
  #establish connection to MySQL. You'll have to change this for your database in the config.json.
  dbConn = MySQLdb.connect(config["Database"]["server"],config["Database"]["username"],config["Database"]["password"],config["Database"]["name"]) or die ("could not connect to database")
  try:
    cursor = dbConn.cursor()
    logging.info('Writing to DB Currency: %s Value: %s', curr, value)
    cursor.execute("INSERT INTO coinacceptor (Currency,Value) VALUES (%s,%s)", (curr,value))
    dbConn.commit() #commit the insert
    cursor.close()  #close the cursor
  except MySQLdb.IntegrityError:
    logging.error('failed to insert data to DB')
  finally:
    cursor.close()  #close just incase it failed

def receiving(ser):
  global last_received
  buffer = ''
  while True:
    #print "waiting..."
    buffer = ser.readline()
    if buffer <> '':
      logging.info('Received: %s', buffer)
      curr = buffer[0:3]
      value = buffer[3:]
      WriteToDB(curr, value)
      curr = ''
      value = 0
      buffer = ''

class SerialData(object):
  def __init__(self, init=50):
    try:
      #check config.json file for the settings of the serial port
      #self.ser = ser = serial.Serial("/dev/ttyUSB0", "9600")
      self.ser = ser = serial.Serial(config["Serial"]["dev"], config["Serial"]["rate"]) 
    except serial.serialutil.SerialException:
      #no serial connection
      self.ser = None
      logging.error('Serial Connection failed')
    else:
      threading.Thread(target=receiving, args=(self.ser,)).start()

  def next(self):
    if not self.ser:
       return 100
    for i in range(40):
      raw_line = last_received
      try:
        return raw_line.strip()
      except ValueError:
        logging.error('Incorrect data: %s',raw_line)
        time.sleep(.005)
    return 0.

  def __del__(self):
    if self.ser:
      self.ser.close()

if __name__=='__main__':
  s = SerialData()
  for i in range(500):
    time.sleep(.015)
