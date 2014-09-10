# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:20:49 2014

@author: genghis
"""

import sys
import string
import logging

from util import mapper_logfile
logging.basicConfig(filename=mapper_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def mapper():

    for line in sys.stdin:
        data = line.strip().split(",")
        if len(data) != 22 or data[6] == 'ENTRIESn_hourly':
            continue
        print '{0}\t{1}'.format(data[1], data[6])


mapper()
