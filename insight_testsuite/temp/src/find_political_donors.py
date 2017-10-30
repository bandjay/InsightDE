# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:00:40 2017

@author: Jay
"""

''' Main class to generate out put files '''
import sys
import os
def main():
    home_path=os.getcwd()
    input_path=os.path.join(home_path,sys.argv[1])
    zip_output_path=os.path.join(home_path,sys.argv[2])
    date_output_path=os.path.join(home_path,sys.argv[3])
    src_path=os.path.join(home_path,"src")
    
    ''' reading input file '''
    lines=open(input_path).readlines()
    req_index=[0,10,13,14,15]
    
    ''' calling by_zip_date module to generate output files '''
    os.chdir(src_path) 
    from by_zip_date import by_zip_date
    zip_obj=by_zip_date(lines,req_index)
    zip_obj._generate_op_file(zip_file_name=zip_output_path,date_file_name=date_output_path)
    
    #print ("output files saved")
    
if __name__ == "__main__":
    main()






