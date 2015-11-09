donation-box
============

open source design/ open source hardware/ open source software

##Software Development
The current software stack of donation box consists of:
        Coin Acceptor Interface
        Serial deamon
        MySQL tables
        WebSocket Server
        Wordpress customization
        
###Coin Acceptor Interface
A simple Arduino code that reads the pulses from the coin acceptor and interprets them to a readable string that is send through the serial. 
For example:
        1 pulse = EUR0.50
        2 pulses = EUR1.00
        4 pulses = EUR2.00

The interface follows the ISO 4217 3 letter code for currencies followed by the value of the coin.

The currency used is defined in the code along with the coins.
The code can run in any Arduino compatible hardware, like the ATTiny, UNO etc.

Files:
        ```
        ATTiny
        arduino/ch_92x_interface_attiny/ch_92x_interface_attiny.ino
        arduino/ch_92x_interface_attiny/notes.h
        Arduino UNO
        arduino/ch_92x_interface_ardu/ch_92x_interface_ardu.ino
        arduino/ch_92x_interface_ardu/notes.h        
        ```

###Serial deamon
A simple deamon in Python that reads on the Serial port, what is send from the Coin Acceptor Interface, (e.g. EUR1.00) and writes the value and currency to the MySQL table "coinacceptor".

Newly insersted coins are inserted to the table with donationid=-1.

Files:
        ```
        Serial2DB.py
        ```
        
###WebSocket Server
A simple deamon in Python that acts as a WebSocket Server communicating with the browser to inform the user of inserted coins and also record donations.
Has two threads, one which is polling the MySQL table "coinacceptor" for new inserted coins which are identified if donationid=-1.
The other thread is the WebSocket server, which hanldes all communication with the browser.
  Sends information about new coins inserted.
  Receives donation and writes the donation information to the "donations" (name,email,project,amount,currency) database table. Gets the donationid given and updates the "coinacceptor" entries with that donationid to mark the coins as donated.
  Prints receipt using the Adafruit_Thermal.py library.

Files:
        ```
        wsServer.py
        ```
###Wordpress customization
The Wordpress includes the installation of the following plugins and further customization is done by widgets and in the header.php file.
Plugins:
        master-slider For having a touch enabled slideshow home screen when displaying multiple projects
        php-code-widget For having php code in some widgets
        qtranslate-x-master For enabling multilingual support on the widgets and on the content
        widget-importer-exporter to easily import & export the widgets
        
####header.php
The main aspect of the added code in the header.php is for the WebSocket client, in Javascript, which updates the UI when new coins are inserted and sends the data to the WebSocket server when the donation button is clicked.
It also has a timer for redirecting the browser to the home page when the donation box is running multiple projects.

####Widgets
- Language Selector widget
- Total amount raised
- Progress Bar
- Days Left
- Donation form
- Home Button
- Info pop up Button
        
Files:
        ```
        wordpress/wp-content/themes/influence-child/header.php
        wordpress/wp-content/themes/influence-child/style.css
        wordpress/donationbox.pi-widgets.wie
        ```
        
##Hardware Development
The hardware is the following:
        Programmable Coin Acceptor
        Arduino compatible microcontroller
        Raspberry Pi 2 + Wifi USB for Access Point
        Tablet
