# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:22:05 2014

@author: genghis
"""

import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():

    riders = 0
    old_key = None
    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) != 2:
            continue
        this_key, count = data
        
        if old_key and old_key != this_key:
            print"{0}\t{1}".format(old_key, riders)
            riders = 0
        old_key = this_key
        riders += float(count)
        
        if old_key != None:
            print "{0}\t{1}".format(old_key, riders)

        
reducer()
