# -*- coding: utf-8 -*-

import tornado.web
import tornado.websocket

class initHandler(tornado.web.RequestHandler):

    def initialize(self, title, html, curtag):
        self.title = title
        self.html = html
        self.cur_tag = curtag 
    
    def get(self):

        self.cur_tag.GetTagDefInfo()
        tagvalue = self.cur_tag.TagSnapshot()

        print('tagvaue', tagvalue)
        print('tagvaue', self.cur_tag.taglist)
        for i in range(len(tagvalue)):
            self.cur_tag.taglist[i]['value'] = '{:.2f}'.format(tagvalue[i])

        print(self.cur_tag.taglist)

        self.cur_tag.clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)

        self.render(self.html, title=self.title, tagname=self.cur_tag.taglist)

    def post(self):
        pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, cur_tag):
        self.cur_tag = cur_tag 
    
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("message received " + message)

    def open(self):
        if self not in self.cur_tag.clients:
            self.cur_tag.clients.append(self)
            self.write_message(u"Connected")
            print("m300exair WS Clients" + str(len(self.cur_tag.clients)))

    def on_close(self):
        if self in self.cur_tag.clients:
            self.cur_tag.clients.remove(self)
            print("m300exair WS Clientse " + str(len(self.cur_tag.clients)))
