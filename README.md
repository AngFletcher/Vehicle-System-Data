# Vehicle System Data
In
## Getting Started
"These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system."
## Hardware Required
   1. Raspberry pi with wifi and bluetooth
   2. ELM327 Bluetooth adapter
   3. Aftermarket head unit and keyboard or laptop with ethernet or vnc capability
   4. 3A power supply
## Prerequisites
Ensure your system is running the most up-to-date software
```
$  sudo apt-get update
$  sudo apt-get upgrade
$  sudo apt-get autoremove
$  sudo reboot
```
Install python-serial
```
$  sudo apt-get install python-serial
```
Then install pyexcel
```
$  pip install pyexcel
```
And finally install the Python GPIO library
```
$  sudo apt-get install python-rpi.gpio
```
## Installing
Pair the Bluetooth device to the Raspberry Pi
```
$  sudo Bluetoothctl
#  power on
#  agent on
#  scan on
#  pair <BT mac address>
```
Enter the pin # if prompted. Most commonly 0000, 1234, or 6789.
```
#  trust <BT mac address>
#  connect <BT mac address>
#  exit
```

Bind the device to the port
 
  Option 1: Bind the device each time the system is booted
```
$  sudo rfcomm release rfcomm0
$  sudo rfcomm bind rfcomm0 <BT mac address>
```
  Option 2: Set the bind command to bind the device automatically
```
$  sudo nano /etc/rc.local
```
  Enter the commands from option 1 before the exit line, save the file and reboot the system.


"A step by step series of examples that tell you have to get a development env running
Say what the step will be
Give the example
And repeat
until finished
End with an example of getting some data out of the system or using it for a little demo"
## Running the tests
"Explain how to run the automated tests for this system
Break down into end to end tests
Explain what these tests test and why
Give an example
And coding style tests
Explain what these tests test and why
Give an example"
## Deployment
"Add additional notes about how to deploy this on a live system"
## Built With
"•	Dropwizard - The web framework used
•	Maven - Dependency Management
•	ROME - Used to generate RSS Feeds"
## Contributing
-
## Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository.
## Authors
•	Angeline Fletcher - Initial work
See also the list of contributors who participated in this project.
## License
-
## Acknowledgments
•	Hat tip to anyone who's code was used
•	Inspiration
•	etc
