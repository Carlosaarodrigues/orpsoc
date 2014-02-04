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


    def clean(self, test):
        utils.launch('make clean', cwd=os.path.join(self.orpsoc_root, test), shell=True)

    def clean_tests(self):
        for test in self.list_tests:
            self.Clean(test)        

