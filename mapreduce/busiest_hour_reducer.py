# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:24:45 2014

@author: genghis
"""

import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    max_entries = 0
    old_key = None
    datetime = ''

    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) != 4:
            continue
        this_key, num_entries, date, time = data
        
        if old_key and old_key != this_key:
            print"{0}\t{1}\t{2}".format(old_key, datetime, max_entries)
            max_entries = 0
            datetime = ''
        
        old_key = this_key
        num_entries = float(num_entries)
        if num_entries >= max_entries:
            max_entries = num_entries
            datetime = "{0} {1}".format(date, time)
            
        if old_key != None:
            print"{0}\t{1}\t{2}".format(old_key, datetime, max_entries)

reducer()