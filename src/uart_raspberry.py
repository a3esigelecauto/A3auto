import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
	timeout=0
)

while True:
    ser.write("\r\nSay something:".encode())
    #rcv = ser.read(10)
    #ser.write(("\r\nYou sent:" + repr(rcv)).encode())
    break
	
	
def uart_send(flag,value):
    if (flag=='m'):
	    ser.write(("m"+str(value)).encode())
    elif (flag=='s'):
	    ser.write(("s"+str(value)).encode())
    else:
        return 1
    return 0
	
def uart_receive_ultrasound():
    return ser.read(ser.in_waiting())
	
#no response from the arduino because it's hard to handle
#it properly without slowing the programm

#no interrupts for the ultrasound yet, just a one-time call
