"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os

try:
    import www.handler.demo_turbine_handler as demo_turbine
except:
    import handler.demo_turbine_handler as demo_turbine

try:
    import www.handler.m300exair_handler as m300exair
except:
    import handler.m300exair_handler as m300exair

# import you handler 

class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")
        
class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
           
            (r"/", indexHandler),
           
            # demo handler
            (r"/demo_tb/", demo_turbine.initHandler),
            (r"/demo_tbwebsocket", demo_turbine.WebSocketHandler),
            
            # add your handler，： 
            (r"/m300exair/", m300exair.initHandler),
            (r"/m300exair_websocket", m300exair.WebSocketHandler),
            
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    mainLoop = tornado.ioloop.IOLoop.instance()
  
    scheduler_demo_tb = tornado.ioloop.PeriodicCallback(demo_turbine.tb_tag.sendmsssage2client, 2000, io_loop=mainLoop)
    scheduler_demo_tb.start()
    
    # add your  scheduler
    
    scheduler_m300exair = tornado.ioloop.PeriodicCallback(m300exair.cur_tag.sendmsssage2client, 2000, io_loop=mainLoop)
    scheduler_m300exair.start()
    
    print('Web Server started! ')
    mainLoop.start()
   
