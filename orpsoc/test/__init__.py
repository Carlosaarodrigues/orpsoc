import os
from orpsoc import utils
from orpsoc.coremanager import CoreManager
from orpsoc.simulator import SimulatorFactory

class Tester(object):
    def __init__(self, test,folder):
        self.orpsoc_root = '/home/carlos/projecto/orpsoc/orpsoc/test'
	self.first = True

        if folder:
            if os.path.exists(folder[0]):
                self.orpsoc_root = folder[0]
            else:
                print "Path " + test[0] + " not found." #fazer uma exception
                exit(1)

        self.list_tests = [d for d in os.listdir(self.orpsoc_root) if os.path.isdir(os.path.join(self.orpsoc_root, d))]

	if "Rom" in self.list_tests:
		self.list_tests.remove("Rom")
		self.list_tests.append("Rom")
        print "root-->  " + str(self.list_tests)

        if test:
            if test[0] in self.list_tests:
	        del self.list_tests[0:len(self.list_tests)]
		self.list_tests.append(test[0])
            else:
                print "Test " + test[0] + " not found. will run all tests"




    def build_C(self, test):
        self.clean(test)
        print " Code C building of test " + test
        utils.launch('make all', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def run(self,system):
	for test in self.list_tests:
            self.build_C(test)

            os.mkfifo(os.path.join(self.orpsoc_root,'RX'))
            os.mkfifo(os.path.join(self.orpsoc_root,'TX'))
            self.fifoRX = open (os.path.join(self.orpsoc_root,'RX'),'r+',0)
            self.fifoTX = open (os.path.join(self.orpsoc_root,'TX'),'w+',0)

            self.elf_file = ['-f', os.path.join(self.orpsoc_root, test) + '/elf_file']
	    self.system = system.system
	    self.sim = system.mode[0]
            if test == "Rom":
	        self.force = True
            self.fifoTX.write("J\n")
            self.run_simulator(self.system, self.sim , self.elf_file)

	    print "Pyton ->" + self.fifoRX.read()
            self.fifoRX.close
            self.fifoTX.close
            os.remove(os.path.join(self.orpsoc_root,'RX'))
            os.remove(os.path.join(self.orpsoc_root,'TX'))


    def run_simulator(self, system, sim, elf_file ):
        core = CoreManager().get_core(system)
        if core == None:
            print("Could not find any core named " + system)
            exit(1)
        sim = SimulatorFactory(sim, core) #por a except se não encontrar o simulador
        if not os.path.exists(sim.sim_root) or self.first:
            sim.configure()
            sim.build()
            self.first = None
	print elf_file
        sim.run(elf_file)


    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)        

