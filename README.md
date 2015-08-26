donation-box
============

Note: The process of setting up your own donation box is still under heavy development and the documentation not complete or detailed enough. If you are still interested in setting it up and can't wait don't hesitate to contact us.


##Description
An open-source screen enabled donation box

The software has three items. 
* The Serial2DB which is a simple deamon written in python which listens on the serial port for messages from the Arduino which is connected to the coin acceptor and writes all entries to an SQL DB.
* The wsServer which is a WebSocket server written in python which reads the SQL DB for new entries and then notifies any connected websocket clients of these. Additionally listens for any donations made and alters accordingly the SQL DB.
* The Wordpress widgets and theme customizations. Which are used for offering an improved user experience based on the design assumption that the wordpress site is running on a 10" tablet. The theme is currently based on Influence and there are several widgets developed to enhance the sidebar. Several plug ins needed for the current implementation and features are already under the plugins folder.

##Setup
###Hardware
The current development is based on the initial following design:
  *A programmable coint acceptor
  *Arduino compatible, connected to the coin acceptor and translating the readings to something more readable (e.g. EUR|2.00)
  *A Raspberry Pi connected through serial to the Arduino and running this software.
  *A tablet that connects through WiFi to the Raspberry Pi (that acts as a hot spot) and loads the Wordpress site.

###Installation
####Arduino
The code for the Arduino to read the coin acceptor will be uploaded soon...

####Raspberry Pi

* Set up DHCP
* Set up DNS
* Set up WiFi access point
* Set up IP forwarding

* Copy repository and start Serial2DB & wsServer.

* Install lighthttpd
* Install MySQL
* Create custom DB tables. Run the create_tables.sql
* Install PHP
* Set up Wordpress
* Add Influence theme 
* Add included child theme & plugins
* Import widgets 

####Android Tablet
* Install Firefox
* Connect to WiFi running on the Pi.
* Load home page


Developed by CommonsLab
