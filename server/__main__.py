import tornado.ioloop
import tornado.options
import tornado.web
import logging

import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line() 
    port = int(os.getenv('PORT'))
    logging.info("starting torando web server on port %d", port) 
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
