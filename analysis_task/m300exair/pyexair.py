# -*- coding: utf-8 -*-
"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""

def exaircoff(o2):
    return 21 / (21 - o2)


def airleakagerate_aph(O2in, O2out):
    """ air leakage rate of the  air preheaters """
    ExAirIn = exaircoff(O2in)
    ExAirOut = exaircoff(O2out)
     
    return (ExAirOut - ExAirIn)
