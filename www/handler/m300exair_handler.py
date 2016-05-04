# -*- coding: utf-8 -*-
"""
Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: MIT
"""
import tornado.web
import tornado.websocket

try:
    from www.handler.gen_taginfo import gentag
except:
    from handler.gen_taginfo import gentag
    
try:
    from www.handler.gen_handler import  initHandler, WebSocketHandler
except:
    from www.handler.gen_handler import  initHandler, WebSocketHandler

cur_tag = gentag("./handler/m300exair_tag.txt")

class initHandler(initHandler):

    def initialize(self):
        self.title = '在线监视客户端： 过量空气系数'
        self.html = "m300exair_ui.html"
        self.cur_tag = cur_tag 

class WebSocketHandler(WebSocketHandler):

    def initialize(self):
        self.cur_tag = cur_tag 
    
  
