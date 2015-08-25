donation-box
============

##Description
An open-source screen enabled donation box

The software has three items. 
* The Serial2DB which is a simple deamon written in python which listens on the serial port for messages from the Arduino which is connected to the coin acceptor and writes all entries to an SQL DB.
* The wsServer which is a WebSocket server written in python which reads the SQL DB for new entries and then notifies any connected websocket clients of these. Additionally listens for any donations made and alters accordingly the SQL DB.
* The Wordpress widgets and theme customizations. Which are used for offering an improved user experience based on the design assumption that the wordpress site is running on a 10" tablet. The theme is currently based on Influence and there are several widgets developed to enhance the sidebar. Several plug ins needed for the current implementation and features are already under the plugins folder.

Developed by CommonsLab
