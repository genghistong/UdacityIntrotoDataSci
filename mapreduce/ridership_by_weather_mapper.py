# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 16:22:58 2014

@author: genghis
"""

import sys
import string
import logging

from util import mapper_logfile
logging.basicConfig(filename=mapper_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def mapper():

    def format_key(fog, rain):
        return '{}fog-{}rain'.format(
            '' if fog else 'no',
            '' if rain else 'no'
        )

    for line in sys.stdin:
        data = line.strip().split(",")
        if len(data) != 22 or data[6] == 'ENTRIESn_hourly':
            continue
        print '{0}\t{1}'.format(format_key(float(data[14]), float(data[15])), data[6])
mapper()
