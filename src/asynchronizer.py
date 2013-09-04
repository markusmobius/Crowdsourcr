import threading
import Queue
import tornado.ioloop

class Asynchronizer(object) :
    def __init__(self, callback_transformer = (lambda x : x)) :  
        self.callback_transformer = callback_transformer
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self.worker)
    def register_callback(self, thunk, callback) :
        self.queue.put((thunk, self.callback_transformer(callback)))
    def worker(self) :
        while True :
            thunk, callback = self.queue.get(block=True)
            callback(thunk())
    def run(self) :
        self.thread.start()

def in_ioloop(callback) :
    def _callback(r) :
        tornado.ioloop.IOLoop.instance().add_callback(lambda : callback(r))
    return _callback
