#!/usr/bin/env python
	
import serial
import time
import string
import io
import os
import sys
import pyexcel as pyex
import fileManip as fm


# open port to pass data
port = serial.Serial('/dev/rfcomm0', 9600)
if(port.isOpen() == False):
        port.open()

#ATE0 intitiate
port.flushInput();
port.timeout = 10
port.write('ATE0\r\n')
port.flush();
port.read(2)

#ATZ check
port.flushInput();
port.write('ATZ\r\n')
port.flush();
response = port.read(20)
if response[9:15] == 'ELM327':
        
        # check available pids 1-20
        port.flushInput();
        port.write('01 00\r\n')
        port.flush();
        pid = port.read(43).split()
        if pid[4] == '.':
            # else use execution list
            pidBin = '111111111111111010100111111100000'
        else:
            pidBin = ''
            pidBin = pidBin + str(pid[7])
            pidBin = pidBin + str(pid[8])
            pidBin = pidBin + str(pid[9])
            pidBin = pidBin + str(pid[10])        
            pidBin = bin(int(pidBin, 16))[2:]
        
        # check available pids 21-40
        if pidBin[31] == '1':
            port.flushInput();
            port.write('01 20\r\n')
            port.flush();
            pid2 = port.read(27).split()
            pidBin2 = ''
            pidBin2 = pidBin2 + str(pid2[4])
            pidBin2 = pidBin2 + str(pid2[5])
            pidBin2 = pidBin2 + str(pid2[6])
            pidBin2 = pidBin2 + str(pid2[7])        
            pidBin2 = bin(int(pidBin2, 16))[2:]
            
        # check vin functions availability
        port.flushInput();
        port.write('09 00\r\n')
        port.flush();
        pid = port.read(30).split()
        if pid[2] == 'NO':
            pidVin = '00000000'
        else:
            pidVin = ''
            pidVin = pidVin + str(pid[5])
            pidVin = pidVin + str(pid[6])
            pidVin = pidVin + str(pid[7])
            pidVin = pidVin + str(pid[8])
            pidVin = bin(int(pidVin, 16))[2:]

        # VIN Decode
        if pidVin[1] == '1':
        
                port.flushInput();
                port.write('09 02\r\n')
                port.flush();
                rawVin = port.read(118).split()                      
                vin1 = unichr(int('0x' + rawVin[8], 0))
                vinNum = ''
                vinNum = vinNum + vin1
                for i in range (12, 16):
                        vin1 = unichr(int('0x' + rawVin[i], 0))
                        vinNum = vinNum + vin1
                for i in range (19, 23):
                        vin1 = unichr(int('0x' + rawVin[i], 0))
                        vinNum = vinNum + vin1
                for i in range (26, 30):
                        vin1 = unichr(int('0x' + rawVin[i], 0))
                        vinNum = vinNum + vin1
                for i in range (33, 37):
                        vin1 = unichr(int('0x' + rawVin[i], 0))
                        vinNum = vinNum + vin1
        else:                        
                # Make / Model background
                vehMake = raw_input('Vin not detected. Enter Vehicle Make: ')
                vehModel = raw_input('Enter Vehicle Model: ')
                vinNum = ('xxxxxxxxx' + vehMake + '-' + vehModel)
        
        # Initialize files 
        fileName = fm.createFile(vinNum)
        file = open(fm.initFile(vinNum), 'r').read()
        engine = float(file[0:3])
        cyl = float(file[4:7])
        sheetName = time.strftime('%Y-%m-%d_%H:%M')+ '.ods'

        if pidBin[9] == '1':
            fm.createBook(fileName, sheetName, '1')
        else:
            fm.createBook(fileName, sheetName, '0')
        
        try:
            while True:
                    # log engine start time if available else use current time
                    if pidBin[30] == '1': 
                        port.flushInput();
                        port.write('01 1F\r\n')
                        port.flush();
                        runTime = port.read(16).split()
                        runTimeA = int(('0x' + runTime[4]), 0)
                        runTimeB = int(('0x' + runTime[5]), 0)
                        runTime = (256*runTimeA) + runTimeB
                    else:
                        runTime = time.strftime('%H:%M:%S')
                        
                    # Short Term Fuel Trim Bank 1
                    if pidBin[5] == '1':    
                        port.flushInput();
                        port.write('01 06\r\n')
                        port.flush();
                        stf1 = port.read(18).split()
                        stf1 = int(('0x' + stf1[4]), 0)
                        stf1 = float((stf1/1.28) -100)
                    else:
                        stf1 = '-'

                    # Long Term Fuel Trim Bank 1
                    if pidBin[6] == '1':    
                        port.flushInput();
                        port.write('01 07\r\n')
                        port.flush();
                        ltf1 = port.read(18).split()
                        ltf1 = int(('0x' + ltf1[4]), 0)
                        ltf1 = float((ltf1/1.28) -100)
                    else:
                        ltf1 = '-'

                    # Short Term Fuel Trim Bank 2
                    if pidBin[7] == '1':    
                        port.flushInput();
                        port.write('01 08\r\n')
                        port.flush();
                        stf2 = port.read(18).split()
                        stf2 = int(('0x' + stf2[4]), 0)
                        stf2 = float((stf2/1.28) -100)
                    else:
                        stf2 = '-'

                    # Long Term Fuel Trim Bank 2
                    if pidBin[8] == '1':    
                        port.flushInput();
                        port.write('01 09\r\n')
                        port.flush();
                        ltf2 = port.read(18).split()
                        ltf2 = int(('0x' + ltf2[4]), 0)
                        ltf2 = float((ltf2/1.28) -100)
                    else:
                        ltf2 = '-'

                    # Fuel Pressure
                    if pidBin[9] == '1':    
                        port.flushInput();
                        port.write('01 0A\r\n')
                        port.flush();
                        fp = port.read(16).split()
                        fp = int(('0x' + fp[4]), 0)
                        fp = float(fp * 3)
                    else:
                        fp = '-'
                        
                    # MPH
                    if pidBin[12] == '1':    
                        port.flushInput();
                        port.write('01 0D\r\n')
                        port.flush();
                        mph = port.read(18).split()
                        mph = (float(int('0x' + mph[4], 0))* 0.621371)
                        mph = round(mph, 1)
                    else:
                        mph = '-'
                              
                    #RPM
                    if pidBin[11] == '1':
                        port.flushInput();
                        port.write('01 0C\r\n')
                        port.flush();
                        rpm = port.read(21).split()
                        rpmA = int(('0x' + rpm[4]), 0)
                        rpmB = int(('0x' + rpm[5]), 0)
                        rpm = (256 * rpmA + rpmB) / 4
                    else:
                        rpm = '-'
                    
                    # Engine Temp
                    if pidBin[4] == '1':    
                        port.flushInput()
                        port.write('01 05\r\n')
                        port.flush();
                        engineTemp = port.read(18).split()
                        engineTemp = float(int(('0x' + engineTemp[4]), 0))
                        engineTemp = engineTemp - 40
                        engineTemp = engineTemp * 9 / 5 + 32
                    else:
                        engineTemp = '-'

                    # Engine load
                    if pidBin[3] == '1':    
                        port.flushInput();
                        port.write('01 04\r\n')
                        port.flush()
                        load = port.read(18).split()
                        load = float(int(('0x' + load[4]), 0))
                        load = load/2.55
                        load = round(load, 1)
                    else:
                        load = '-'

                    # Throttle Position
                    if pidBin[16] == '1':          
                        port.flushInput();
                        port.write('01 11\r\n')
                        port.flush();
                        tps = port.read(18).split()
                        tps = float(int(('0x' + tps[4]), 0))
                        tps = tps/2.55
                        tps = round(tps, 1)
                    else:
                        tps = '-'
                                    
                    # Fuel system status
                    if pidBin[2] == '1':    
                        port.flushInput()
                        port.write('01 03\r\n')
                        port.flush();
                        fst = port.read(21).split()
                        fst = int(('0x' + fst[4]), 0)
                        fst1 = fm.fstDecode(fst)
                    else:
                        fst1 = '-'
                                       
                    #intake air temperatue
                    if pidBin[14] == '1':          
                        port.flushInput()
                        port.write('01 0F\r\n')
                        port.flush();
                        iat = port.read(18).split()
                        iat = float(int('0x' + iat[3], 0) - 40) # celsius
                        IAT = iat * (9/5) + 32 # fahrenheit
                    else:
                        IAT = '-'

                    # mass airflow sensor / map sensor
                    if pidBin[15] == '1':    
                        port.flushInput();
                        port.write('01 10\r\n')
                        port.flush();
                        maf = port.read(16).split()
                        mafA = float(int('0x' + maf[3], 0))
                        mafB = float(int('0x' + maf[4], 0))
                        maf = float(int((256 * mafA + mafB) / 100))
                        maf1 = str(maf)

                    elif pidBin[10] == '1':
                        port.flushInput();
                        port.write('01 0B\r\n')
                        port.flush();
                        map = port.read(18).split()
                        map = float(int(('0x' + map[3]), 0))
                    else:
                        map = '-'

                    # O2 sensor readings 1-8
                    if pidBin[19] == '1':
                        port.flushInput();
                        port.write('01 14\r\n')
                        port.flush();
                        o2A = port.read(21).split()
                        o2Avolt = float(int('0x' + o2A[3], 0))/200
                        o2Atrim = float(int('0x' + o2A[4], 0))
                        o2Atrim = (100/128)*o2Atrim -100
                    else:
                        o2Avolt = '-'
                        o2Atrim = '-'
    
                    if pidBin[20] == '1':
                        port.flushInput();
                        port.write('01 15\r\n')
                        port.flush();
                        o2B = port.read(21).split()
                        o2Bvolt = float(int('0x' + o2B[4], 0))/200
                        o2Btrim = float(int('0x' + o2B[5], 0))
                        o2Btrim = (1/12.8)*o2Btrim -100
                    else:
                        o2Bvolt = '-'
                        o2Btrim = '-'

                    if pidBin[21] == '1':
                        port.flushInput();
                        port.write('01 16\r\n')
                        port.flush();
                        o2C = port.read(21).split()
                        o2Cvolt = float(int('0x' + o2C[4], 0))/200
                        o2Ctrim = float(int('0x' + o2C[5], 0))
                        o2Ctrim = (1/12.8)*o2Ctrim -100
                    else:
                        o2Cvolt = '-'
                        o2Ctrim = '-'
                    
                    if pidBin[22] == '1':
                        port.flushInput();
                        port.write('01 17\r\n')
                        port.flush();
                        o2D = port.read(21).split()
                        o2Dvolt = float(int('0x' + o2D[4], 0))/200
                        o2Dtrim = float(int('0x' + o2D[5], 0))
                        o2Dtrim = (1/12.8)*o2Dtrim -100
                    else:
                        o2Dvolt = '-'
                        o2Dtrim = '-'

                    if pidBin[23] == '1':
                        port.flushInput();
                        port.write('01 18\r\n')
                        port.flush();
                        o2E = port.read(21).split()
                        o2Evolt = float(int('0x' + o2E[4], 0))/200
                        o2Etrim = float(int('0x' + o2E[5], 0))
                        o2Etrim = (1/12.8)*o2Etrim -100
                    else:
                        o2Evolt = '-'
                        o2Etrim = '-'

                    if pidBin[24] == '1':
                        port.flushInput();
                        port.write('01 19\r\n')
                        port.flush();
                        o2F = port.read(21).split()
                        o2Fvolt = float(int('0x' + o2F[4], 0))/200
                        o2Ftrim = float(int('0x' + o2F[5], 0))
                        o2Ftrim = (1/12.8)*o2Ftrim -100
                    else:
                        o2Fvolt = '-'
                        o2Ftrim = '-'

                    if pidBin[25] == '1':
                        port.flushInput();
                        port.write('01 1A\r\n')
                        port.flush();
                        o2G = port.read(21).split()
                        o2Gvolt = float(int('0x' + o2G[4], 0))/200
                        o2Gtrim = float(int('0x' + o2G[5], 0))
                        o2Gtrim = (1/12.8)*o2Gtrim -100
                    else:
                        o2Gvolt = '-'
                        o2Gtrim = '-'

                    if pidBin[26] == '1':
                        port.flushInput();
                        port.write('01 1B\r\n')
                        port.flush();
                        o2H = port.read(21).split()
                        o2Hvolt = float(int('0x' + o2H[4], 0))/200
                        o2Htrim = float(int('0x' + o2H[5], 0))
                        o2Htrim = (1/12.8)*o2Htrim -100
                    else:
                        o2Hvolt = '-'
                        o2Htrim = '-'             
                        

                    # append data to book
                    lambdaAppend = [runTime, o2Avolt, o2Atrim, o2Bvolt, o2Btrim, o2Cvolt, o2Ctrim, o2Dvolt, o2Dtrim, o2Evolt, o2Etrim, o2Fvolt, o2Ftrim, o2Gvolt, o2Gtrim, o2Hvolt, o2Htrim]
                    fuelAppend = [runTime, fp, stf1, ltf1, stf2, ltf2, fst1]
                     
                    if pidBin[15] == '1':
                        mafGenAppend = [runTime, mph, rpm, engineTemp, load, tps, maf, IA]
                        fm.appendBook(fileName, sheetName, mafGenAppend, fuelAppend, lambdaAppend)
                    else:
                        mapGenAppend = [runTime, mph, rpm, engineTemp, load, tps, map, IAT]
                        fm.appendBook(fileName, sheetName, mapGenAppend, fuelAppend, lambdaAppend)
                   
        except KeyboardInterrupt:
            exit
else:
    print('No Connection to Bluetooth.')
    
port.close()
