from tornado.web import RequestHandler, Application, url
from tornado.ioloop import IOLoop
from tornado import gen
from motor import MotorClient

import time

class TodoListHandler(RequestHandler):

  def fetch_todo_list(self):
    db = self.settings['db']
    cursor = db.todo.find()
    time.sleep(3) # simulates a lengthy operation
    return cursor.to_list(length=100)

  @gen.coroutine
  def get(self):
    todo_list = yield self.fetch_todo_list()
    self.render('todo_list.html', title='Todo List', todos=todo_list)


#Entry point of the whole program
def main():
  import os.path
  cur_dir = os.path.dirname(__file__)
  static_path = os.path.join(cur_dir, 'static')
  template_path = os.path.join(cur_dir, 'templates')
  db = MotorClient('mongodb://localhost').test

  settings = dict(
    static_path=static_path,
    template_path=template_path,
    db=db,
    debug=True, #Comment this out when deploy to the production
  )

  app = Application([
    url(r"^/todo_list/?$", TodoListHandler),
  ], **settings)

  app.listen(8888)
  print "Listening on 8888..."
  IOLoop.current().start()

if __name__ == "__main__":
  main()
