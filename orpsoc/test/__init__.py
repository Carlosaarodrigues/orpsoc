import os
import imp
import subprocess
import time
from orpsoc import utils
from orpsoc.coremanager import CoreManager
from orpsoc.simulator import SimulatorFactory
from orpsoc.build import BackendFactory
from orpsoc.config import Config

class Tests_path(Exception): # tests path dont found
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Test(Exception): # test dont found
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class OpenOCD (Exception): # problem launch openocd
     def __init__(self, cmd):
         self.cmd = cmd
     def __str__(self):
         return repr(self.cmd)

class Load_sof (Exception): # problem load sof file
     def __init__(self, cmd):
         self.cmd = cmd
     def __str__(self):
         return repr(self.cmd)

class Mode (Exception): # mode dont found
     def __init__(self, mode):
         self.mode = mode
     def __str__(self):
         return repr(self.mode)

class System (Exception): # system dont found
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Connect_OpenOCD(Exception): # Problem connecting with OpenOCD
     def __init__(self, host,port):
         self.host = host
         self.port = port
     def __str__(self):
         return repr(self.host, self.port)

class Serial_port (Exception): # Serial pornto dont found
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Configue_Verilator(Exception): # dont configure file of verialtor
     def __init__(self, uart, new_uart):
         self.uart = uart
         self.new_uart = new_uart
     def __str__(self):
         return repr(self.uart, self.new_uart)


class Tester(object):
    def __init__(self, test, alternative_tests_root):
        self.tests_root = os.path.join(Config().orpsoc_root,'orpsoc/test')
        self.openocd_root = Config().openocd_root
        self.system_root = Config().systems_root
	self.first = True

        if not os.path.exists(self.tests_root):
            raise Tests_path ("default: " + self.tests_root)

        if alternative_tests_root:
            if os.path.exists(alternative_tests_root[0]):
                self.tests_root = alternative_tests_root[0]
            else:
                raise Tests_path (alternative_tests_root[0])

        self.list_tests = [d for d in os.listdir(self.tests_root) if os.path.isdir(os.path.join(self.tests_root, d))]

	if "Rom" in self.list_tests:
	    self.list_tests.remove("Rom")
	    self.list_tests.append("Rom")

        if test:
            if test[0] in self.list_tests:
	        del self.list_tests[0:len(self.list_tests)]
		self.list_tests.append(test[0])
            else:
                raise Test (test[0])


    def build_C(self, test, equip):
        self.clean(test)
        print "Building C " + test + " test for " + equip
        print 'make ' + equip 
        utils.launch('make ' + equip , cwd=os.path.join(self.tests_root, test), shell=True)


    def run(self,system):

        self.system = system.system
        self.mode = system.mode[0]
	self.sof_file = "build/" + self.system + "/bld-quartus/" + self.system + ".sof"

        self.result = open (os.path.join(self.tests_root,'restults'),'w+',0)
        self.result.write("tests with " + self.mode+ '\n')

        args = ['-rf']
        args += ['build/'+self.system]
        #utils.launch('rm',args)

        if self.mode == 'board':
            #build verilog
            #self.run_build(self.system) #descomentar isto

            #send .sof for board
            if not os.path.exists(self.sof_file):
                raise Load_sof (self.sof_file)
            cmd = "quartus_pgm --mode=jtag -o p\;" + self.sof_file
            os.system(cmd) 


            #lauch OpenOCD
            print self.openocd_root
            args = ['./src/openocd']
            args += ['-s']
            args += ['./tcl']
            args += ['-f']
            args += ['./tcl/interface/altera-usb-blaster.cfg']
            args += ['-f']
            args += ['./tcl/board/or1k_generic.cfg']
            try:
                self.process = subprocess.Popen(args,cwd = self.openocd_root)
            except OSError:
                raise OpenOCD(args)

            time.sleep(5)

        if self.mode == 'verilator':
            self.configure_verilator( self.system, self.mode)

	for test in self.list_tests:

            imp.load_source('Pe_test', os.path.join(self.tests_root,test) + '/test.py')
            import Pe_test
            if self.mode == 'verilator':
                Pe_test.verilator(self,test)
            elif self.mode == 'icarus':
                Pe_test.icarus(self,test)
            elif self.mode == 'board':
                Pe_test.board(self,test)
            else:
                raise Mode (self.mode)

        self.result.close()
        if self.mode == 'board':
            self.process.terminate() 


    def run_simulator(self, system, sim, elf_file = None ):
        core = CoreManager().get_core(system)
        if core == None:
            raise system (system)
        sim = SimulatorFactory(sim, core)
        if  not os.path.exists(sim.sim_root) or self.first:
            sim._write_config_files()
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
            raise system (system)


    def configure_verilator(self, system, sim):
        self.uart = os.path.join(self.system_root, system) + "/bench/verilator/UartSC.cpp"
        self.new_uart = os.getcwd() + os.path.join("/build/", system) + "/sim-verilator/bench/verilator/UartSC.cpp"
        core = CoreManager().get_core(system)
        if core == None:
            raise system (system)
        sim = SimulatorFactory(sim, core)
	sim.configure()

        if not os.path.exists(self.uart) or not os.path.exists(self.new_uart):
            raise Configue_Verilator (self.uart, self.new_uart)

        cmd = "sed 's/\/\/#define UART_FIFO/#define UART_FIFO/' " + self.uart + " > " + self.new_uart
        os.system(cmd)


    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.tests_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)       

