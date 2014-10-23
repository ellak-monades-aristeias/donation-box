#!/usr/bin/python
####################################################
# Name: Donation Box deamon 
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

last_received = ''

def WriteToDB(curr, value):
  #establish connection to MySQL. You'll have to change this for your database.
  dbConn = MySQLdb.connect("localhost","root","c0mm0ns","wordpress") or die ("could not connect to database")
  try:
    cursor = dbConn.cursor()
    print "Writing to DB Currency: %s Value: %s" % (curr, value)
    cursor.execute("INSERT INTO coinacceptor (Currency,Value) VALUES (%s,%s)", (curr,value))
    dbConn.commit() #commit the insert
    cursor.close()  #close the cursor
  except MySQLdb.IntegrityError:
    print "failed to insert data to DB"
  finally:
    cursor.close()  #close just incase it failed

def receiving(ser):
  global last_received
  buffer = ''
  while True:
    buffer = ser.readline(ser.inWaiting())
    if buffer <> '':
      print "Received: %s" % buffer
      curr = buffer[0:3]
      value = buffer[3:]
      WriteToDB(curr, value)
      curr = ''
      value = 0
      buffer = ''

class SerialData(object):
  def __init__(self, init=50):
    try:
      self.ser = ser = serial.Serial('/dev/pts/1', 9600)
    except serial.serialutil.SerialException:
      #no serial connection
      self.ser = None
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
        print 'Incorrect data',raw_line
        time.sleep(.005)
    return 0.

  def __del__(self):
    if self.ser:
      self.ser.close()
 
if __name__=='__main__':
  s = SerialData()
  for i in range(500):
    time.sleep(.015)
