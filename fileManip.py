#!/usr/bin/env python
	
import serial
import time
import string
import io
import os
import sys
import stat
import pyexcel as pyex

def createFile (vinNum):
    os.chdir('/home')
    vinPath = os.path.join('/home/pi/OBDii/', vinNum[9:])
    if not os.path.exists(vinPath):
        os.makedirs(vinPath)
    fileName=time.strftime('%Y-%m-%d-%H:%M')+'.obs'
    return vinPath

def initFile (vin):
    os.chdir('/home')
    vinPath = os.path.join('/home/pi/OBDii/', vin[9:])
    if os.path.isfile(os.path.join(vinPath, 'initFile.txt')):
            initPath=os.path.join(vinPath, 'initFile.txt')
    else:
        engine = input('Enter the engine size in liters: ')
        cylinders = input('Enter the number of cylinders: ')
        cyl = engine/cylinders
        engine = str(engine) + '\n'
        cyl = str(cyl) + '\n'
        initPath = os.path.join(vinPath, 'initFile.txt')
        with open(initPath, 'a') as file:
            file.writelines([engine, cyl]) 
    return initPath

def createBook (filePath, bookName, books):
    os.chdir('/home')
    os.chdir(filePath)
    if books == '1':
        book = { 'Lambda Data':
                        [
                            ['Time', 'Sensor 1 Voltage', 'Sensor 1 STFT', 'Sensor 2 Voltage', 'Sensor 2 STFT', 'Sensor 3 Voltage',
                             'Sensor 3 STFT', 'Sensor 4 Voltage', 'Sensor 4 STFT', 'Sensor 5 Voltage', 'Sensor 5 STFT',
                             'Sensor 6 Voltage', 'Sensor 6 STFT', 'Sensor 7 Voltage', 'Sensor 7 STFT', 'Sensor 8 Voltage',
                             'Sensor 8 STFT']
                        ],
                    'Fuel System Data':
                        [
                            ['Time', 'Fuel Pressure', 'Short Term Fuel Trim (STFT) 1', 'Long Term Fuel Trim (LTFT) 1',
                             'Short Term Fuel Trim (STFT) 2', 'Long Term Trim (LTFT) 2', 'Fuel Status']
                        ],
            
                    'General Data':
                        [
                            ['Time', 'MPH', 'RPM', 'Engine Temp(F)', 'Engine Load(%)', 'Throttle Position', 'MAF',
                             'Intake Air Temp(F)']
                        ]

        }
    else:
        book = { 'Lambda Data':
                        [
                            ['Time', 'Sensor 1 Voltage', 'Sensor 1 STFT', 'Sensor 2 Voltage', 'Sensor 2 STFT', 'Sensor 3 Voltage',
                             'Sensor 3 STFT', 'Sensor 4 Voltage', 'Sensor 4 STFT', 'Sensor 5 Voltage', 'Sensor 5 STFT',
                             'Sensor 6 Voltage', 'Sensor 6 STFT', 'Sensor 7 Voltage', 'Sensor 7 STFT', 'Sensor 8 Voltage',
                             'Sensor 8 STFT']
                        ],
                    'Fuel System Data':
                        [
                            ['Time', 'Fuel Pressure', 'Short Term Fuel Trim (STFT) 1', 'Long Term Fuel Trim (LTFT) 1',
                             'Short Term Fuel Trim (STFT) 2', 'Long Term Trim (LTFT) 2', 'Fuel Status']
                        ],
            
                    'General Data':
                        [
                            ['Time', 'MPH', 'RPM', 'Engine Temp(F)', 'Engine Load(%)', 'Throttle Position', 'MAP',
                             'Intake Air Temp(F)']
                        ]
        }
    
    inBook = pyex.Book(book)
    inBook.save_as(bookName)
    return

def appendBook (filePath, bookName, genSheet, fuelSheet, lambdaSheet):
    os.chdir('/home')
    os.chdir(filePath)
    book = pyex.load_book(bookName)
    book["General Data"].row += genSheet
    book["Fuel System Data"].row += fuelSheet
    book["Lambda Data"].row += lambdaSheet
    book.save_as(bookName)
    return

def fstDecode(pid):
    if pid == 1:
        return 'Open loop due to insufficient engine temperature'
    elif pid == 2:
        return 'Closed loop, using oxygen sensor feedback to determine fuel mix'
    elif pid == 4:
        return 'Open loop due to engine load OR fuel cut due to deceleration'
    elif pid == 8:
        return 'Open loop due to system failure'
    elif pid == 16:
        return 'Closed loop, using at least one oxygen sensor but there is a fault in the feedback system'