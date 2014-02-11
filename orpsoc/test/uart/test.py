import os
def verilator(self):

    self.result.write("Test Uart -->")
    word = "Uart Test\n"

    #create and open fifos
    os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
    os.mkfifo(os.path.join(self.orpsoc_root,'TX'))
    self.fifoRX = os.open (os.path.join(self.orpsoc_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)
    self.fifoTX = open (os.path.join(self.orpsoc_root,'TX'),'w+',0)

    self.fifoTX.write(word)
    self.run_simulator(self.system, 'verilator' , self.elf_file)

    self.data = os.read(self.fifoRX,11)
    if self.data == word:
        print "Test Uart --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test Uart --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(self.fifoRX)
    self.fifoTX.close
    os.remove(os.path.join(self.orpsoc_root,'RX'))
    os.remove(os.path.join(self.orpsoc_root,'TX'))


def icarus(self):
    print "Test not developed for icarus"

def board(self):
    print "Test in developing for board"

    print "Board must be connect!!"

    self.result.write("Test Uart -->")
    #building

