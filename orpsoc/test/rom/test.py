import os
def verilator(self):

    self.result.write("Test ROM-->")
    #config test bench files

    #create and open fifos
    os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
    self.fifoRX = os.open (os.path.join(self.orpsoc_root,'RX'),os.O_RDONLY | os.O_NONBLOCK)

    #force Build
    self.first = True
    self.run_simulator(self.system, 'verilator' , self.elf_file)

    self.data = os.read(self.fifoRX,11)
    if self.data == "Rom OK\n":
        print "Test ROM --> PASS"
        self.result.write(" PASS\n")
    else:
        print "Test ROM --> FAIL"
        self.result.write(" FAIL\n")

    #close and remove fifos
    os.close(self.fifoRX)
    os.remove(os.path.join(self.orpsoc_root,'RX'))


def icarus(self):
    print "Test not developed for icarus"

def board(self):
    print "Test not developed for board"

