# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:23:41 2014

@author: genghis
"""

import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():

    riders = 0      # The number of total riders for this key
    num_hours = 0   # The number of hours with this key
    old_key = None

    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) != 2:
            continue
        this_key, count = data
        
        if old_key and old_key != this_key:
            print"{0}\t{1}".format(old_key, float(riders/num_hours))
            riders = 0
            num_hours = 0
        old_key = this_key
        riders += float(count)
        num_hours += 1
        
        if old_key != None:
            print "{0}\t{1}".format(old_key, float(riders/num_hours))

reducer()
