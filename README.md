# Vehicle System Data
Today's vehicles have a variety of modules that regulate everything from fuel delivery and ignition timing to Windshield wiper speed and air conditioning controls. One such modules, the Electronic Control Unit (ECU), receives information from a variety of sensors and uses the information to control engine performance. Abnormalities in engine performance are stored as trouble codes. Beginning in 1996 all vehicles produced in North America are required to be equipped with an Onboard Diagnostics II (OBDII) that uses one communication protocol and connector for universal access. Diagnostic tools to access stored trouble codes have become more accessable to the average do-it-yourselfer, but tools to read live data remain more costly than the average person is willing to invest. This project utilizes a J9141-2 compatible ELM327 OBDII Bluetooth adapter paired with a Bluetooth capable Raspberry Pi to access and record fuel and emission system data.
Sensors logged: Vehicle Run Time, MPH, RPM, Engine Temperature(F), Manifold Absolute Pressure(MAP), Mass Air Flow(MAF), Intake Air Temperature (F), Throttle Position(%), Engine Load(%), Fuel Pressure, Short Term Fuel Trim Bank 1, Long Term Fuel Trim Bank 1, Short Term Fuel Trim Bank 2, Long Term Fuel Trim Bank 2, Fuel System Status, Oxygen Sensor Voltage (Banks 1-8), Oxygen Sensor Fuel Trim (Banks 1-8)
****Note - Not all vehicles will support all sensors****
## Hardware Required
   1. Raspberry pi with wifi and bluetooth
   2. J9141-2 compatible ELM327 Bluetooth adapter
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
## Initial Setup

## Running the tests
"Explain how to run the automated tests for this system
Break down into end to end tests
Explain what these tests test and why
Give an example
And coding style tests
Explain what these tests test and why
Give an example"
## Deployment
This program can be adapted for headless deployment only on vehicles that support VIN decode and only after the initial setup has been completed. If the vehicle does not support VIN decode the user will be promped to enter the vehicle make and model each time the program is started for logging purposes. 
## Authors
•	Angeline Fletcher - Initial work
## License
-
## Acknowledgments
•	Hat tip to anyone who's code was used
•	Inspiration
•	etc
