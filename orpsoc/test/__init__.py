import os
import imp
import subprocess
import time
from orpsoc import utils
from orpsoc.coremanager import CoreManager
from orpsoc.simulator import SimulatorFactory
from orpsoc.build import BackendFactory
from orpsoc.config import Config

class Tests_path(Exception): # não contra o caminho de testes
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Test(Exception): # não encontra o teste
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class OpenOCD (Exception): # não conetra o openocd
     def __init__(self, cmd):
         self.cmd = cmd
     def __str__(self):
         return repr(self.cmd)

class Load_sof (Exception): # não concegue carregar o soffile
     def __init__(self, cmd):
         self.cmd = cmd
     def __str__(self):
         return repr(self.cmd)

class Mode (Exception): # nao encotnra o mode
     def __init__(self, mode):
         self.mode = mode
     def __str__(self):
         return repr(self.mode)

class System (Exception): # nao encotra o sistema
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Tester(object):
    def __init__(self, test, alternative_tests_root):
        self.tests_root = os.path.join(Config().orpsoc_root,'orpsoc/test')
        self.openocd_root = Config().openocd_root
        self.system_root = Config().systems_root
	self.first = True

        if alternative_tests_root:
            if os.path.exists(alternative_tests_root[0]):
                self.tests_root = alternative_tests_root[0]
            else:
                raise Tests_path (alternative_tests_root[0]) #adicionar orpsoc

        self.list_tests = [d for d in os.listdir(self.tests_root) if os.path.isdir(os.path.join(self.tests_root, d))]

	if "Rom" in self.list_tests:
		self.list_tests.remove("Rom")
		self.list_tests.append("Rom")

        if test:
            if test[0] in self.list_tests:
	        del self.list_tests[0:len(self.list_tests)]
		self.list_tests.append(test[0])
            else:
                raise Test (test[0]) #adicionar orpsoc


    def build_C(self, test, equip):
        self.clean(test)
        print "Building C " + test + " test for " + equip
        print 'make ' + equip 
        utils.launch('make ' + equip , cwd=os.path.join(self.tests_root, test), shell=True)


    def run(self,system):

        self.system = system.system
        self.mode = system.mode[0]

        self.result = open (os.path.join(self.tests_root,'restults'),'w+',0)
        self.result.write("tests with " + self.mode+ '\n')

        args = ['-rf']
        args += ['build/'+self.system]
        #utils.launch('rm',args)

        if self.mode == 'board':
            #build verilog
            #self.run_build(self.system) #descomentar isto

            #send .sof for board
            cmd = "quartus_pgm --mode=jtag -o p\;build/" + self.system + "/bld-quartus/" + self.system + ".sof"
            try:
                os.system(cmd) 
            except:
                raise Load_sof (cmd)

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
        sim = SimulatorFactory(sim, core) #por a excetpio do simulador
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
        core = CoreManager().get_core(system)
        if core == None:
            raise system (system)
        sim = SimulatorFactory(sim, core)
	sim.configure()

        cmd = "sed 's/\/\/#define UART_FIFO/#define UART_FIFO/' " + os.path.join(self.system_root, system) + "/bench/verilator/UartSC.cpp > " + os.getcwd() + os.path.join("/build/", system) + "/sim-verilator/bench/verilator/UartSC.cpp"
        os.system(cmd) #exception se não encontrar um dos ficheiros


    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.tests_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)       

