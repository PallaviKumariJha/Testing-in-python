#!/usr/bin/python2

import os
import sys
import ConfigParser
from optparse import OptionParser

COMPILED = {'cpp':'g++', 'c':'gcc'}
INTERPRETED = {'py':'python'}

def parse_file_name(filename):
    """Module to get the file extention"""
    return filename.rpartition('.')[0], filename.rpartition('.')[-1]

class FILE(object):
    def openfile(self, editor, filename):
        """ Module which opens a file """
        command = [editor, filename]
        command = ' '.join(command)    
        os.system(command)

    def compilefile(self, compiler, init, extention, compile_option,filename):
        """Module which takes care of compilation"""
        if compile_option == True:
            command = [compiler, '-o', init, filename]
            command = ' '.join(command)
            return_val = os.system(command)
            return return_val
        
        elif compile_option == False:
            print "To compile the program change the option."
        
        else:
            print "No option set in the file."


    def output(self, init, run_option, return_val = 0):
        """ Module for the execution of compiled file"""
        if run_option == True:
            run_command = ['./', init]
            run_command = ''.join(run_command)
            chmod_command = ['chmod', '+x', init]
            chmod_command = ' '.join(chmod_command)
            if return_val == 0:
                os.system(chmod_command)
                os.system(run_command)
        
        elif run_option == False:
            print "To execute the program change the option."

        else:
            print "No option is set."  
   

class CmdLine(object):
    def parsecommandline(self):
        """Module to parse command line"""
        parser = OptionParser()
        parser.add_option("-e", "--editor", dest = "editor", help = "Change the file editor" )
        parser.add_option("-c", "--compile", dest = "cmdline_compile_opt", help = "Choose compiling option", action="store_false")
        parser.add_option("-r", "--runas", dest = "cmdline_execution_opt", help = "Choose execution option", action="store_false")         
        (options,args) = parser.parse_args()
        return options, args[0] 



class ConfigFile(object):                   # configuration file should be existing in the home directory
    def read_config(self):
        """Module to read the configuration file"""
        home_path = os.path.expanduser('~')
        file_path = [home_path, '/sourcefile.conf']
        file_path = ''.join(file_path)
        config = ConfigParser.RawConfigParser()
        config.read(file_path)
        return config

    def set_config(self):
        """Module to set the configuration options from file"""   
        config = self.read_config()
        editor = config.get('Editor', 'editor')
        run_option = config.get('run_option', 'run')
        compile_option = config.get('run_option', 'compile')
        return (editor, compile_option, run_option)
                   
class FinalConfig(CmdLine, ConfigFile):
    def final_config(self):
        editor, compile_option, run_option = self.set_config()
        options, filename = self.parsecommandline()        

        if compile_option == 'no':
            compile_opt = False
        elif compile_option == 'yes':
            compile_opt = True
    
        if run_option == 'no':
            run_opt = False   
        elif run_option == 'yes':
            run_opt = True        

        if options.cmdline_compile_opt == False: 
            compile_opt = options.cmdline_compile_opt
            
        if options.cmdline_execution_opt == False:
            run_opt = options.cmdline_execution_opt

        if options.editor != None:
            editor = options.editor

        return (editor, compile_opt, run_opt, filename)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./test3.py <filename>"
        exit(1)
    
    finalconfig = FinalConfig()
    editor, compile_option, run_option, filename = finalconfig.final_config()

    init, extention = parse_file_name(filename)

    File = FILE()
    File.openfile(editor, filename)

    if extention in COMPILED:
        return_val = File.compilefile(COMPILED[extention], init, extention,compile_option,filename)
        if return_val == 0:
            File.output(init, run_option, return_val)
        else:
            print "Unsuccesful compilation"

    if extention in INTERPRETED:
        File.output(filename, run_option)

        
