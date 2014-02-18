import os
def verilator(self,test):

    self.result.write("Test ROM-->")
    #config test bench files

    self.build_C(test,'sim')
    elf_file = ['-f', os.path.join(self.orpsoc_root, test) + '/elf_file_sim']

    #create and open fifos
    os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
    RX = os.open (os.path.join(self.orpsoc_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)

    #force Build
    self.first = True
    self.run_simulator(self.system, 'verilator' , elf_file)

    result = os.read(RX,11)
    if result == "Rom OK\n":
        print "Test ROM --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test ROM --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(RX)
    os.remove(os.path.join(self.orpsoc_root,'RX'))


def icarus(self,test):
    print "Test not developed for icarus"

def board(self,test):

    word = "Uart Test\n"

    print "Board must be connect!!"
    print "OpenOCD must be build for board"

    self.result.write("Test ROM -->")
    #build elf_file
    self.build_C(test,'board')
    elf_file = os.path.join(self.orpsoc_root, test) + '/elf_file_board'

    print "open Serial Port(UART)"
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) # ver da excetpiom

    print 'connecting OpenOCD'
    HOST = '127.0.0.1'   #localhost
    PORT = 6666    #OpenOCD port for machine interface
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))

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

    print "wait for data"
    time.sleep(1)
    result = ser.read(size=64)

    if result == "Rom OK\n":
        print "Test ROM --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test ROM --> FAIL"
        self.result.write(" FAIL\n")

    ser.close()


