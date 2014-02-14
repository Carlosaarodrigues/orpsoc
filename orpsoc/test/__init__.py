import os
import imp
import subprocess
import time
from orpsoc import utils
from orpsoc.coremanager import CoreManager
from orpsoc.simulator import SimulatorFactory
from orpsoc.build import BackendFactory

class Tester(object):
    def __init__(self, test,folder):
        self.orpsoc_root = '/home/carlos/projecto/orpsoc/orpsoc/test'
	self.first = None

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

        if test:
            if test[0] in self.list_tests:
	        del self.list_tests[0:len(self.list_tests)]
		self.list_tests.append(test[0])
            else:
                print "Test " + test[0] + " not found. will run all tests"




    def build_C(self, test, equip):
        self.clean(test)
        print "Building C " + test + " test for " + equip
        print 'make ' + equip 
        utils.launch('make ' + equip , cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def run(self,system):
        self.result = open (os.path.join(self.orpsoc_root,'restults'),'w+',0)
        self.result.write("tests with " + system.mode[0]+ '\n')

        self.system = system.system

        if system.mode[0] == 'board':
            #build verilog
            #self.run_build(self.system) #descomentar isto
            #send soft_elf "quartus_pgm --mode=jtag -o p\;build/"system"/bld-quartus/de0_nano.sof"

            cmd = "quartus_pgm --mode=jtag -o p\;build/" + self.system + "/bld-quartus/de0_nano.sof"
            #os.system(cmd) #descomentar

            print "lauch OpenOCD"
            args = ['./src/openocd']
            args += ['-s']
            args += ['./tcl']
            args += ['-f']
            args += ['./tcl/interface/altera-usb-blaster.cfg']
            args += ['-f']
            args += ['./tcl/board/or1k_generic.cfg']
            #self.process = subprocess.Popen(args,cwd ='/home/carlos/projecto/openocd') # descomentar isto

            time.sleep(5)

	for test in self.list_tests:

            imp.load_source('Pe_test', os.path.join(self.orpsoc_root,test) + '/test.py')
            import Pe_test
            if system.mode[0] == 'verilator':
                Pe_test.verilator(self,test)
            if system.mode[0] == 'icarus':
                Pe_test.icarus(self,test)
            if system.mode[0] == 'board':
                Pe_test.board(self,test)

        self.result.close()
        if system.mode[0] == 'board':
            #self.process.terminate() #descomentar
            print "aqui"

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
        sim.run(elf_file)

    def run_build(self,system):
        if system in CoreManager().get_systems():
            core = CoreManager().get_core(system)
            backend = BackendFactory(core.system)
            backend.configure()
            backend.build()
        else:
            print("Error: Can't find system " + known.system)


    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)       

