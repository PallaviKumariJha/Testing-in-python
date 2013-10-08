import unittest
import simple
import os
import random
import ConfigParser
from optparse import OptionParser

class TestFILE(unittest.TestCase):
    def setUp(self):
        self.TestFILEobj = simple.FILE()

    def test_openfile(self):  
        try:
            realSystem = os.system
            called = []
            def stubSystem(command):
                if command == ("vim " + "t1.c"):
                    called.append(True)
            os.system = stubSystem              # mocking the vim launcher    
            self.TestFILEobj.openfile('vim', 't1.c') # function under test
            assert(called == [True])
        
        finally:
            os.system = realSystem
    
    def test_compilefile_choose(self):   #this test runs with the original file ('t1.c' in this case)
        compile_opt = False
        return_val = self.TestFILEobj.compilefile('g++', 't1', 'c', compile_opt, 't1.c')   
        self.assertEquals(None, return_val)
        compile_opt = True
        return_val = self.TestFILEobj.compilefile('g++', 't1', 'c', compile_opt, 't1.c')
        self.assertEquals(0, return_val)
        
    def test_compilefile_sample(self):
        compile_opt_list = [False, True]
        return_val_list = [0, None]
        random.shuffle(compile_opt_list)
        return_val = self.TestFILEobj.compilefile('g++', 't1', 'c', compile_opt_list[0], 't1.c')  
        self.assertTrue(return_val in return_val_list)
        
        
    def test_output(self):
        try:
            realSystem = os.system
            called1 = []
            called2 = []
            
            def chmod_stubSystem(chmod_command):
                if chmod_command == 'chmod ' + '+x ' + 't1':
                    called1.append(True)
            
            def run_stubSystem(run_command):
                if run_command == './' + 't1':
                    called2.append(True)
            
            os.system = chmod_stubSystem  # mocking the chmod operation 
            self.TestFILEobj.output('t1', True, 0)
            assert(called1 == [True])
            
            os.system = run_stubSystem  #mocking the run operation
            self.TestFILEobj.output('t1', True, 0)
            assert(called2 == [True])
            
        finally:
            os.system = realSystem                         
   
class TestConfigFile(unittest.TestCase):
    def setUp(self):
        self.TestConfigobject = simple.ConfigFile()
    
    def test_read_config(self):
        try:
            config = ConfigParser.RawConfigParser()
            realSystem = config.read 
            called = []
            
            def stubSystem(file_path):
                home_path = os.path.expanduser('~')
                file_path = [home_path, '/sourcefile.conf']
                if file_path == ''.join(file_path):
                    called.append(True)
                    
                config = ConfigParser.RawConfigParser()
                config.read = stubSystem
                self.TestConfigobject.read_config()
                assert(called == [True])
                
        finally:
            config.read = realSystem  
              
    def test_set_config(self):
        editor, compile_option, run_option = self.TestConfigobject.set_config()                        
        test_editor = ['vim', 'nano', 'vi']
        test_options = ['yes', 'no']
        self.assertTrue(editor in test_editor)
        self.assertTrue(compile_option in test_options)
        self.assertTrue(run_option in test_options)

class TestCmdLine(unittest.TestCase):
    def setUp(self):
        self.TestCmdLineobj = simple.CmdLine()
    
    def testparsecommandline(self):
        """Module to parse command line"""
        parser = OptionParser()
        parser.add_option("-e", "--editor", dest = "editor", help = "Change the file editor" )
        parser.add_option("-c", "--compile", dest = "cmdline_compile_opt", help = "Choose compiling option", action="store_false")
        parser.add_option("-r", "--runas", dest = "cmdline_execution_opt", help = "Choose execution option", action="store_false")         
        (options,args) = parser.parse_args()
        return options, 't.c'   # 't.c' is a real existing file in the parent directory 
    
    def test_parsecommandline(self):
        try:
            realfunction = self.TestCmdLineobj.parsecommandline
            
            def mockfun():
                options, filename = self.testparsecommandline()
                return (options, filename)            
            
            options, filename = mockfun()
            self.assertEquals(filename, 't.c')
            self.assertFalse(options.cmdline_compile_opt)
            self.assertFalse(options.cmdline_execution_opt)
        
        finally:
            self.testparsecommandline = realfunction



class TestFinalConfig(unittest.TestCase):
    def setUp(self):
        self.TestFinalConfigobject = simple.FinalConfig() 
        self.TestCmdLineobject = simple.CmdLine()
        self.TestConfigFileobject = simple.ConfigFile()      
        
    def testparsecommandline(self):
        """Module to parse command line"""
        parser = OptionParser()
        parser.add_option("-e", "--editor", dest = "editor", help = "Change the file editor" )
        parser.add_option("-c", "--compile", dest = "cmdline_compile_opt", help = "Choose compiling option", action="store_false")
        parser.add_option("-r", "--runas", dest = "cmdline_execution_opt", help = "Choose execution option", action="store_false")         
        (options,args) = parser.parse_args()
        return options, 't.c'    #Here filename is 't.c' which is a real existing file.

    def test_final_config(self):
        try:
            realfunction1 = self.TestCmdLineobject.parsecommandline
            realfunction2 = self.TestConfigFileobject.set_config
            def mockfun1():
                options, filename = self.testparsecommandline()    
                return (options, filename)                
                
            def mockfun2():
                editor, compile_option, run_option = 'vim', 'yes', 'yes'
                return (editor, compile_option, run_option)
                
            self.TestCmdLineobject.parsecommandline = mockfun1  
            self.TestConfigFileobject.set_config = mockfun2
            editor, compile_option, run_option = mockfun2()
            options, filename = mockfun1()
            self.assertEquals('vim', editor)
            self.assertTrue(compile_option)
            self.assertTrue(run_option)                   
                            
                                
        finally:
            self.TestCmdLineobject.parsecommandline = realfunction1
            self.TestConfigFileobject.set_config = realfunction2
            


unittest.main()    

      
    
    
        
  
