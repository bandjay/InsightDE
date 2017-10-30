# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 09:29:35 2017

@author: Jay
"""

from collections import defaultdict
from heapq import heappush as push, heappushpop as pushpop
import datetime

''' 
Class to generate required output files based on group by zip and date 

Steps:
1) Data structure chosen is a dictionary of dictionaries with max_heap,min_heap lists for median calculation and 
   count of total transactions,total of donations received.
2) Read one record at a time from input file and simulataenously update dictionaries for by zipcode and by date cases    
3) For by zip code case whenever a new record is read , dictionary gets updated and running median is calculated 
   and results will be written to the output file
4) For by transaction date case for every record dictionary gets updated but output file is generated at the end.
    
''' 

class by_zip_date:
    
    ''' Initializing constructor with lines read from input file '''    
    def __init__(self,lines,req_index):
        self.lines = lines
        self.req_index = req_index
    
    ''' Method to validate Zip code '''    
    def _is_good_zip(self):
        try:
            return self.fields[4] == "" and self.fields[0] != "" and self.fields[1] != "" \
                    and self.fields[3] != "" and len(self.fields[1]) >= 5
        except:
            return False
    
    ''' Method to validate Transaction date '''    
    def _is_good_date(self):
        try:
            m,d,y = int(self.fields[2][0:2]),int(self.fields[2][2:4]),int(self.fields[2][4:])
            datetime.datetime(y,m,d)
            date_flag = True
            return self.fields[4] == "" and self.fields[0] != "" and self.fields[3] != "" \
                    and date_flag and len(self.fields[2]) == 8
        except:
            return False
    
    ''' Method for updating dictionary data structure '''       
    def _update_dict(self,key,dict_):        
        self.fields[3] = int(self.fields[3])
        if key in dict_.keys():            
            value = self.fields[3]
            value = pushpop(dict_[key]['max_heap'], value)
            value = -pushpop(dict_[key]['min_heap'], -value)
            if len(dict_[key]['max_heap']) <= len(dict_[key]['min_heap']):
                push(dict_[key]['max_heap'], value)
                dict_[key]['cnt'] += 1
                dict_[key]['Total'] += self.fields[3]
            else:
                push(dict_[key]['min_heap'], -value)
                dict_[key]['cnt'] += 1
                dict_[key]['Total'] += self.fields[3]
        else:
            push(dict_[key]['max_heap'],self.fields[3])
            dict_[key]['cnt'] = 1
            dict_[key]['Total'] = self.fields[3]

    ''' Method for finding median using updated dictionaries '''    
    def _find_median(self,key,dict_): 
        max_heap_len = len(dict_[key]['max_heap'])
        min_heap_len = len(dict_[key]['min_heap'])
        if max_heap_len > min_heap_len:
            return str(round(dict_[key]['max_heap'][0]))
        else:
            return str(round((dict_[key]['max_heap'][0] - dict_[key]['min_heap'][0])/2))
        
    ''' Method to generate output files '''
    def _generate_op_file(self,zip_file_name,date_file_name):  
        
        ''' Initializing two dictionary data structures '''
        date_dict = defaultdict(lambda: defaultdict(list))
        zip_dict = defaultdict(lambda: defaultdict(list))
        
        ''' Updating dictionaries for each record and generating output files '''
        with open(zip_file_name,"w") as zfile , open(date_file_name,"w") as dfile: 
            
            ''' for median values by zip output file '''
            for l in self.lines:
                self.fields = [e for i,e in enumerate(l.split("|")) if i in self.req_index] 
                if self._is_good_zip():
                    key = self.fields[0] + "|" + self.fields[1][0:5]
                    
                    ''' updateing zip dictionaty '''
                    self._update_dict(key,zip_dict)
                    
                    ''' Calculating running median '''
                    median = self._find_median(key,zip_dict)
                    
                    ''' writing to median by zipcode file '''
                    zfile.write(key + "|" + median + "|" + str(zip_dict[key]['cnt']) + "|"+ 
                                str(zip_dict[key]['Total']) + "\n")
                    #print ("Yes zip")
                else:
                    pass
                    #print ("NO zip")
                
                ''' updating date dictionary '''
                if self._is_good_date():
                    Dkey = self.fields[0] + "|" + self.fields[2]
                    self._update_dict(Dkey,date_dict)
                    #print ("Yes Date",Dkey,date_dict[Dkey]['Total'],date_dict[Dkey]['cnt'])
                else:
                    pass
                    #print ("No Date")
                    
            ''' writing to median by date file '''        
            for k in sorted(date_dict.keys()):
                dmedian = self._find_median(k,date_dict)
                dfile.write( k + "|" + dmedian + "|" + str(date_dict[k]['cnt']) + "|" + 
                            str(date_dict[k]['Total']) + "\n")
             
            #print(date_dict)
            #print(zip_dict)