import os
import socket
import serial
from orpsoc import utils
def verilator(self,test):

    self.result.write("Test Uart -->")

    self.build_C(test,'sim')
    elf_file = ['-f', os.path.join(self.orpsoc_root, test) + '/elf_file_sim']

    word = "Uart Test\n"

    #create and open fifos
    os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
    os.mkfifo(os.path.join(self.orpsoc_root,'TX'))
    RX = os.open (os.path.join(self.orpsoc_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)
    TX = open (os.path.join(self.orpsoc_root,'TX'),'w+',0)

    TX.write(word)
    self.run_simulator(self.system, 'verilator' , elf_file)

    Rdata = os.read(RX,11)
    if Rdata == word:
        print "Test Uart --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test Uart --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(RX)
    TX.close
    os.remove(os.path.join(self.orpsoc_root,'RX'))
    os.remove(os.path.join(self.orpsoc_root,'TX'))


def icarus(self,test):
    print "Test not developed for icarus"

def board(self,test):
    print "Test in developing for board"

    print "Board must be connect!!"
    print "OpenOCD must be build for board"

    self.result.write("Test Uart -->")

    self.build_C(test,'board')
    elf_file = os.path.join(self.orpsoc_root, test) + '/elf_file_board'

    print "send elf_file and run program in board"
    print 'connecting OpenOCD'
    HOST = '127.0.0.1'   # Symbolic name meaning the local host
    PORT = 6666    # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.send('poll\x1a')
    print "1"
    data= s.recv(1024)
    print "halt"
    print data.replace('\x1a','\n')
    s.send('load_image '+ elf_file)
    print "image" 
    s.send('reg npc 0x100')
    print "reg"
    s.send('resume')
    print "resume"

##    print "send data"
  ##  try:
    #    ser = serial.Serial(port, 9600, timeout=1)
    #    ser.write("ati")
    #    time.sleep(3)
    #    read_val = ser.read(size=64)
    #    print read_val
    #    if read_val is not '':
    #       print port
    #except serial.SerialException:
    #    exit(1)

    print "wait for data"


