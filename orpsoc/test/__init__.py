import os
from orpsoc import utils

class Tester(object):
    def __init__(self):
        self.orpsoc_root = '../orpsoc/orpsoc/test'
        self.list_tests = [d for d in os.listdir(self.orpsoc_root) if os.path.isdir(os.path.join(self.orpsoc_root, d))]
	if self.list_tests.index("Rom"):
		self.list_tests.remove("Rom")
		self.list_tests.append("Rom")
        print "root-->  " + str(self.list_tests)





    def build_C(self, test):
        self.clean(test)
        print " Code C building of test " + test
        utils.launch('make all', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def run(self):
	for test in self.list_tests:
             self.build_C(test)

    def run_simluator(self):
        logger.debug('sim() *Entered*')
        core = CoreManager().get_core(known.system)
        if core == None:
                print("Could not find any core named " + known.system)
                exit(1)
        if known.sim:
                sim_name = known.sim[0]
        elif core.simulators:
                sim_name = core.simulators[0]
        else:
                print("No simulator was found in "+ known.system + " core description")
                logger.error("No simulator was found in "+ known.system + " core description")
                exit(1)
        try:
                sim = SimulatorFactory(sim_name, core)
        except DependencyError as e:
                print("Error: '" + known.system + "' or any of its dependencies requires '" + e.value + "', but this core was not found")
                exit(1)
        if known.force or not os.path.exists(sim.sim_root):
                sim.configure()
                sim.build()
                sim.run(remaining)



    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)        

