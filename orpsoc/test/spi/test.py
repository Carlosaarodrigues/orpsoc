import os
def verilator(self):

    self.result.write("Test SPI-->")

    #create and open fifos
    os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
    self.fifoRX = os.open (os.path.join(self.orpsoc_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)

    self.run_simulator(self.system, 'verilator' , self.elf_file)

    self.data = os.read(self.fifoRX,11)
    if self.data == "SPI OK\n":
        print "Test SPI --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test SPI --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(self.fifoRX)
    os.remove(os.path.join(self.orpsoc_root,'RX'))


def icarus(self):
    print "Test not developed for icarus"

def board(self):
    print "Test not developed for board"

