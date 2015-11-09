donation-box
============

open source design/ open source hardware/ open source software

##Installation
The installation of a donation box contains the assembly of the box and connecting the electronic components.

###Assembling the box
1. Start by putting one of the side pieces flat on a surface with the grooves on top.
2. Screw the angles for the bottom, back and front panels.
3. Place the bottom, front and back panels and screw them on the angles
4. Put lock and hinges on door.
5. Put Raspberry Pi and shield on place and screw it.
6. Prepare SD card and place it in Raspbery Pi
7. Connect USB Wifi dongle to Raspberry Pi .
8. Put coin acceptor in place and connect cable on the shield.
9. Put thermal printer in place and connect cable on the shield.
10. Place tablet and secure it in place.
11. Put power supply and connect to shield, Raspberry Pi and tablet.
12. Put box for falling coins in place.

##Turning on Donation Box
Make sure power supply, thermal printer, coin acceptor are connected.
Then plug in power. Raspberry Pi will turn on and boot automatically.
Wait for about 2 minutes and then turn on the tablet and look for the DonationBox Wifi.
Once connected go to Firefox browser and go to http://donationbox.pi URL. 

##Adding new project
This can be done from the tablet but it will be easier if you connect to the DonationBox Wifi from a laptop/PC.
1. Go to http://donationbox.pi/wp-admin URL and log in.
2. Create new Post.
3. Edit post and upload a featured image. Select category "Project" for post. 
4. Publish post.

##Home page
If you want to run the donation box for a single project then just set the post as home page from the theme customizer.
When setting the donation box for running multiple projects you need to create a page and set it as home page.
Set up a slider using the master slider plug in and place this slider on the page created and set as home.

NOTE: Configuring the box for single or multiple projects has to be set currently in several places (header.php & widgets).
Soon the process will be updated and simplified.

##Troubleshooting
Coming soon
