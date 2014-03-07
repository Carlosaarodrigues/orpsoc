import os
import socket
import serial
import time
from orpsoc import utils
from orpsoc.test import Connect_OpenOCD, Serial_port

def verilator(self,test):

    self.result.write("Test SPI-->")

    self.build_C(test,'sim')
    elf_file = ['-f', os.path.join(self.tests_root, test) + '/elf_file_sim']

    #create and open fifos
    try:
        os.mkfifo(os.path.join(self.tests_root,'RX'))
    except OSError:
        os.remove(os.path.join(self.tests_root,'RX'))
        os.mkfifo(os.path.join(self.tests_root,'RX'))
    RX = os.open (os.path.join(self.tests_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)

    self.run_simulator(self.system, 'verilator' , elf_file)

    Result = os.read(RX,11)
    if Result == "SPI OK\n":
        print "Test SPI --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test SPI --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(RX)
    os.remove(os.path.join(self.tests_root,'RX'))


def icarus(self,test):
    print "Test not developed for icarus"

def board(self,test):

    #serial port
    self.serial_port = '/dev/ttyUSB0'
    self.baudrate = 115200
    #connect OpenOCD machine interface
    self.host = '127.0.0.1'
    self.port = 6666 

    self.result.write("Test SPI -->")
    #build elf_file
    self.build_C(test,'board')
    elf_file = os.path.join(self.tests_root, test) + '/elf_file_board'

    print "open Serial Port(UART)"
    if not os.path.exists(self.serial_port):
        raise Serial_port (self.serial_port)

    try:
        ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
    except serial.SerialException:
        print 'change permission of ' + self.serial_port
        os.system('sudo chmod a+rwx' + self.serial_port)
        ser = serial.Serial(self.serial_port , self.baudrate, timeout=1)
        

    print 'connecting OpenOCD'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((self.host,self.port))
    except socket.error:
        raise Connect_OpenOCD (self.host,self.port)

    print "send elf_file and run program in board"
    #halt processor
    s.send('halt\x1a')
    s.recv(1024)

    #load elf_file
    s.send('load_image '+ elf_file +'\x1a')
    s.recv(1024) 

    #change program point for 0x100
    s.send('reg npc 0x100\x1a')
    s.recv(1024)

    #start processor
    s.send('resume\x1a')
    s.recv(1024)

    while 50:
        time.sleep(1)
        Result = ser.read(size=64)
        print Result

    ser.close()

