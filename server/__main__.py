import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import asynchronous
import tornado.gen as gen
import logging
import asyncmongo

import os
import re

# parse the mongo connection URL
mongodb_url = os.getenv('MONGOHQ_URL', "http://localhost/test")
r=re.match(r"mongodb://((?P<dbuser>\w+):(?P<dbpass>\w+)@)?(?P<host>[\w.]+)(:(?P<port>\d+))?/(?P<dbname>\w+)", mongodb_url)

mdb_connection_params = dict(
  pool_id=r.group('dbname'),
  dbuser= r.group('dbuser'),
  dbpass= r.group('dbpass'),
  host=   r.group('host'),
  port=   r.group('port') and int(r.group('port')) or 27017,
  dbname= r.group('dbname'),
  maxcached=10,
  maxconnections=50
)

class Handler(tornado.web.RequestHandler):
    @property
    def db(self):
      if not hasattr(self, '_db'):
        logging.info(str(mdb_connection_params))
        self._db = asyncmongo.Client(**mdb_connection_params)
        return self._db

class MainHandler(Handler):
  @asynchronous
  @gen.engine
  def get(self):
      res = yield gen.Task(self.db.monkeys.find)
      self.write("Hello, cruel world")
      self.write("%s" % list(res))
      self.finish()

application = tornado.web.Application([
    (r"/", MainHandler),
], debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line() 

    port = int(os.getenv('PORT', 8000))
    application.listen(port)
    logging.info("starting torando web server on port %d", port) 
    tornado.ioloop.IOLoop.instance().start()
