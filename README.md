donation-box
============

open source design/ open source hardware/ open source software

Note: The process of how to set up your own donation box is still under heavy development and the documentation not complete or detailed enough yet. If you are anyhow interested in building and setting up your own box and you can't wait, don't hesitate to contact us.

##Idea
During the last few years, especially in Greece, many communities and initiatives have tried to do things in many different fields of interest. Often times, these teams will sooner or later need some funding in order to fulfill their goals. Some of them organize events, some run online crowdfunding campains and some also find several new ways to cover their needs.
From our experience, online crowdfunding does not work as expected, most of the time. People are hesitating to put all their details online, especially if they choose to donate a small amount, or some may not have a debit or credit card to do that. Eventually, most of these people prefer to give their donations in cash, in person or into a physical box somewhere. Of course, many donation boxes, usually managed by NGOs, already exist in public places, shops and such places. The problem with these boxes is that they do not offer much information about the organization that asks for money, nor do they offer transparency about what happens to the donations, who are the organization, or how much money they need.
Due to the lack of possible ways to convey sufficient information, traditional donation boxes are not being used by teams that focus on a specific project, because people can not understand what the project exactly is.
In order to solve the above problems, we came up with the idea of a screen-enabled interactive donation box.
The box can run several projects or causes that are asking for donations. It provides information (text, images, video) for each project. It provides real-time information about the progress (donations accepted, donations needed, finishing date). Donations are recorded and if users choose so, they can be registered to keep in touch with the project for which they donated.
The box also can issue receipts for each donation.
Connecting several donation boxes to an online service can add more value to each box and all the projects that are running, as a project can be created online and activated in several boxes in several locations simultaneously.
This way, we hope to help NGOs, social initiatives and others, to achieve their goals and their fulfil their ideas. By offering a platform for crowdfunding that exists in physical, public spaces, we are offering a different and more direct connection between projects asking for help and people willing to help.

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
##Developers
More detailed [Developers Manual](DevelopersManual.md).

##Users
More detailed [Users Manual](UserManual.md).

Developed by CommonsLab
