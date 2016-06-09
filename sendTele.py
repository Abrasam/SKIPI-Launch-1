import serial, crcmod, datetime
from time import sleep
from yoctopuce.yocto_api import *
from yoctopuce.yocto_genericsensor import *
checksum = crcmod.predefined.mkCrcFun('crc-ccitt-false')
def makeTelemetry(gpsData):
    data = gpsData.split(",")
    if len(data) > 9 and "GGA" in data[0]:
        id = datetime.datetime.now() - datetime.datetime(1970, 1, 1)
        id = int(id.total_seconds())
        lat = ("-" if data[3] == "S" else "") +  data[2]
        long = ("-" if data[5] == "W" else "") + (data[4])
        alt = data[9]
        sats = data[7]
        time = data[1][0:2] + ":" + data[1][2:4] + ":" + data[1][4:6]
        intensity = 0
        try:
            intensity = float("{0:.2f}".format(getLightIntensity()))
        except:
            pass
        telemetry = "$$SKIPI," + str(id) + "," + time + "," + lat + "," + long + "," + alt + "," + sats + "," + str(intensity)
        csum = (hex(checksum(telemetry[2:],0xFFFF))).upper()
       # print(csum)
        telemetry += "*" + csum[2:] + "\n"
        return telemetry
    return ""
def getLightIntensity():
    errmsg=YRefParam()
    YAPI.RegisterHub("usb",errmsg)
    genericsensor = YGenericSensor.FindGenericSensor("RXMVOLT1-645E6.genericSensor1")
    if genericsensor.isOnline():
        voltage = genericsensor.get_currentValue()
        print(str(voltage))
        kiloWattsPerSquareMetre = voltage/33.29
        return kiloWattsPerSquareMetre * 1000
    return 0
for i in range(0, 5):
    data = ""
    with serial.Serial("/dev/ttyAMA0", 9600, timeout=1) as g:
        g.flush()
        data = g.readline()
        start = datetime.datetime.now().second
        while not ("GGA" in data):
                data = g.readline()
                if datetime.datetime.now().second - start > 3:
                     break
        g.flush()
        g.baudrate = 75
        sleep(1)
    with serial.Serial("/dev/ttyAMA0", 75, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO) as r:
        if "GGA" in data:
            # print(r.baudrate)
            r.flush()
            telemetry = makeTelemetry(data)
            #print(datetime.datetime.now())
            for c in telemetry:
                b = bytes(c)
                r.write(b)
            r.flush()
            #print(datetime.datetime.now())
            print("==========================================TRANSMISSION==========================================")
            print(telemetry[::-1][1:][::-1])
            print("================================================================================================")
            sleep(1)
