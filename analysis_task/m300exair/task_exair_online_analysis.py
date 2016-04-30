# -*- coding: utf-8 -*-
"""
Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""
from datetime import datetime
import codecs

from db.pyredis import TagDefToRedisHashKey, tagvalue_redis, SendToRedisHash
from analysis_task.m300exair.pyexair import exaircoff

class UnitExaircoff:

    def __init__(self, tagin, tagout):
        self.ailist = []
   
        file = codecs.open(tagin, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid}) 
      
    
        self.aolist = []
        file = codecs.open(tagout, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.aolist.append({'id':tagid, 'desc':desc, 'value':None, 'ts':None}) 
 
    def setouttag(self):
        TagDefToRedisHashKey(self.aolist)
 
    def Onlinecal(self):
        o2 = float(self.ailist[0]['value']) 
        cur_exaircoff =exaircoff(o2)
        self.aolist[0]['value'] = cur_exaircoff
    
    def run(self):
        tagvalue_redis(self.ailist)
        self.Onlinecal()
        curtime = datetime.now()
        for tag in self.aolist:
            tag['ts'] = curtime 

        SendToRedisHash(self.aolist)

        tagvalue_redis(self.aolist)
        
        for tag in self.aolist:
            print(tag['desc'], tag['value'])

