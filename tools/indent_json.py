#!/usr/bin/env python
# -*- coding: utf-8 
"""
An ugly script that auto-indentes JSON files.

Takes as arguments the absolute path of the input directory which contains the 
JSON files and the absolute path of output directory which will contains the 
auto-indented / generated JSON files.

Example::

    $ ./indent_json '/home/user/Desktop/input_dir' '/home/user/Desktop/output_dir'
    
Input directory must only contains JSON files.

"""
import os, sys, simplejson

def main():
    args = sys.argv[1:]
    input_dir, output_dir = args
    files = os.listdir(input_dir)
    for f in files:
        input_file = os.path.join(input_dir, f)
        output_file = os.path.join(output_dir, f)
        load = simplejson.load(file(input_file))
        dump = simplejson.dumps(load, sort_keys=True, indent=4)
        output_file = open(output_file, 'w')
        for l in dump:
            output_file.write(l)
        output_file.close()
        
if __name__ == '__main__':
    main()

