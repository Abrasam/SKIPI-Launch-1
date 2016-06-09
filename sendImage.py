import serial, subprocess, datetime
from timeout import *
with open("output.bin", "rb") as f:
    try:
        bytes = f.read(256)
        while bytes != "":
            print("Sending image packet.")
            with serial.Serial("/dev/ttyAMA0", 75, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO) as r:
                r.flush()
                r.write(bytes)
                r.flush()
                print("Sent 256 bytes of image.")
                bytes = f.read(256)
            try:
                with timeout(seconds=90):
                    subprocess.call(["python /home/pi/HAB/sendTele.py"], shell=True)
            except TimeoutError:
                    print("Telemetry timed out.")
    finally:
        print("Image sending ended.")
