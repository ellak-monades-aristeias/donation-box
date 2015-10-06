donation-box
============

Note: The process of setting up your own donation box is still under heavy development and the documentation not complete or detailed enough. If you are still interested in setting it up and can't wait don't hesitate to contact us.

##Idea
The last few years, especially in Greece, many initiatives have tried to do things in many different fields of interest. Many times these teams sooner or later will need some funding in order to fulfill their goals. Some of them do events, some run online crowdfunding campains and also find several new ways to cover their needs.
From our experience the online crowdfunding, most of the time, does not work as expected. People are hesitating to put all their details online, especially if they are opting to donate a small amount, or some may not have a debit or credit card to do that. While most of these people will prefer to give their donations in person or in a physical box somewhere. Many donation boxes of course already exist usually managed by NGOs that are put in public places, shops etc. The problem with these boxes is that they do not offer information and transparency. What is the organization? How much money they need? 
Also this way is not being used by teams that are focused on a specific project, because of the lack to inform the people of what the project is.
So to try and solve the above problems we came up with the idea of a screen enabled donation box.
The box can run several projects/causes that are asking for donations. It provides information (text, images, video) for each project. It provides real-time information about the progress (donations accepted, donations needed, finishing date). Donations are recorded and if users choose can be registered to keep in touch with the project in which they donated.
The box also can issue receipts for each donation.
Connecting several donation boxes to a cloud service can add more value to each box and all the projects that are running. A project can be created online and activated in several boxes in several locations.
This way we hope to help NGOs, social initiatives and others, with completing their ideas. By offering a platform for crowdfunding that is in physical public spaces offering a different more direct connection between projects asking for help and people willing to help.

##Description
An open-source screen-enabled donation box

The software has three parts. 
  1. The Serial2DB which is a simple daemon written in python. It listens on the serial port for messages from the Arduino, which is connected to the coin acceptor, and it writes all entries to an SQL DB.
  2. The wsServer which is a WebSocket server written in python. It watches the SQL DB for new entries and notifies any connected websocket clients of these changes. Additionally it listens for any donations made through the WebUI and alters the SQL DB accordingly.
  3. The Wordpress widgets and theme customizations are used for offering an improved user experience. The design is based on the assumption that the Wordpress site is displayed on a 10-inch screen. The theme is currently based on Influence and there are several widgets developed to enhance the sidebar. Several plug-ins, needed for the current implementation and features, can be found in the plugins folder.

##Setup
###Hardware
The current development is based on the initial following design:
  * A programmable coint acceptor
  * Arduino compatible, connected to the coin acceptor and translating the readings to something more readable (e.g. EUR|2.00)
  * A Raspberry Pi connected through serial to the Arduino and running this software.
  * A tablet that connects through WiFi to the Raspberry Pi (that acts as a hot spot) and loads the Wordpress site.

###Installation
####Arduino
The code for the Arduino to read the coin acceptor will be uploaded soon...

####Raspberry Pi

  * Set up DHCP
  * Set up DNS
  * Set up WiFi access point
  * Set up IP forwarding
  * Install python tornado
  * [Printer] sudo apt-get install python-serial python-imaging python-unidecode
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
