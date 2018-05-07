## Vehicle System Data
Today's vehicles have a variety of modules that regulate everything from fuel delivery and ignition timing to windshield wiper speed and air conditioning controls. One such module, the Electronic Control Unit (ECU), receives information from a variety of sensors and uses the information to control engine performance. Abnormalities in engine performance are stored as trouble codes. Beginning in 1996 all vehicles produced in North America are required to be equipped with an Onboard Diagnostics II (OBDII) that uses one communication protocol and connector for universal access. Diagnostic tools to access stored trouble codes have become more accessable to the average do-it-yourselfer, but tools to read live data remain more costly than the average person is willing to invest. This project utilizes a J9141-2 compatible ELM327 OBDII Bluetooth adapter paired with a Bluetooth capable Raspberry Pi to access and record fuel and emission system data.

Sensors logged by this program: Vehicle Run Time, MPH, RPM, Engine Temperature(F), Manifold Absolute Pressure(MAP), Mass Air Flow(MAF), Intake Air Temperature (F), Throttle Position(%), Engine Load(%), Fuel Pressure, Short Term Fuel Trim Bank 1, Long Term Fuel Trim Bank 1, Short Term Fuel Trim Bank 2, Long Term Fuel Trim Bank 2, Fuel System Status, Oxygen Sensor Voltage (Banks 1-8), Oxygen Sensor Fuel Trim (Banks 1-8)

****Note - Not all vehicles support all sensors****

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
The first time a program is executed on a new vehicle the program will obtain data from the user.
The program will present 1 of 2 options depending on the supported system in the vehicle.

Option 1:
	The vehicle supports the protocol that relays VIN information.
	![HondaInitScreen.PNG](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/HondaInitScreen.PNG)

Option 2:
	The vehicle does not support the VIN protocol
	![](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/JeepInitScreen1.PNG)

Once Vehicle data is obtained the program will create a file labeled OBDii to hold vehicles and a vehicle specific file to store the data logged.
![](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/FileInit.PNG)

The program can be ended at any time with a keyboard interrupt (ctrl-c).
## Deployment
Once initial setup is complete the program will create an initFile.txt file and a .obs book which contains three spreadsheets - General Data, Fuel System Data, and Lambda Data where each sheet contains a snapshot of sensors at labeled intervals.

Program Execution:
![Execute.PNG](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/Execute.PNG)


General Data:     
![GeneralData.PNG](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/GeneralData.PNG)

Fuel System Data:
![](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/FuelData.PNG)

Lambda Data:
![](https://github.com/AngFletcher/Vehicle-System-Data/blob/master/LambdaData.PNG)

## Adaptions
This program can be adapted for headless deployment only on vehicles that support VIN decode and only after the initial setup has been completed. If the vehicle does not support VIN decode the user will be promped to enter the vehicle make and model each time the program is started for logging purposes. 
## Authors
•	Angeline Fletcher - Initial work
## Acknowledgments
•	The program utilizes the following libraries:

pyserial [https://pythonhosted.org/pyserial/](https://pythonhosted.org/pyserial/)
    
pyexcel [https://pypi.org/project/pyexcel/](https://pypi.org/project/pyexcel/)

## Resources
The following websites were used for reseach and inspiration:

https://en.wikipedia.org/wiki/OBD-II_PIDs

http://blog.brianhemeryck.me/how-to-interface-with-your-cars-ecu-through-obd2-and-python/

http://www.lightner.net/lightner/bruce/Lightner-183.pdf

https://x-engineer.org/automotive-engineering/internal-combustion-engines/performance/calculate-volumetric-efficiency/

http://pyexcel.readthedocs.io/en/latest/index.html

