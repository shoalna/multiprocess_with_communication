import multiprocessing
import random
import time
import queue
import os
try:
    import process
except ImportError:
    from . import process
from signal import SIGTERM
from server import app

"""
1. use event to detect predict finish
2. set max length for queue.
   The predict requset more than max should got response like 'too busy'
"""


class ApiService(multiprocessing.Process):
    def __init__(self, host, port, queue, request_dict, response_dict):
        multiprocessing.Process.__init__(self)
        self.host = host
        self.port = port

        # self._server = None
        # self._loop = None
        # self._process = None

        self.queue = queue
        self.request_dict = request_dict
        self.response_dict = response_dict

    def run(self):
        print("Running server")
        app.ctx.req_queue = self.queue
        app.ctx.req_dict = self.request_dict
        app.ctx.res_dict = self.response_dict
        app.run(host=self.host, port=self.port, workers=2)

    # def stop(self):
    #     os.kill(self._process.pid, SIGTERM)
    #     print("Stopping server")
    #     self._process.join()
    #     self._process.terminate()


class Predictor(multiprocessing.Process):
    def __init__(self, queue, request_dict, response_dict):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.request_dict = request_dict
        self.response_dict = response_dict

    def run(self):
        print("Hosting Predictor.calc")

        while True:
            try:
                req = self.queue.get(timeout=3)
            except queue.Empty:
                print("the queue is empty, waiting...")
                continue

            if req is process._sentinel:
                self.queue.put(process._sentinel)
                break

            print(f"Predictor try get: {req} from {self.request_dict}")
            print("Start run Predictor.calc")
            t1 = time.time()
            req = list(self.request_dict.keys())[0]
            self.request_dict.pop(req)
            rn = random.randint(1, 3)
            process.hprocess(rn=rn)
            self.response_dict[req] = rn
            print("Predictor run rn: {}, use time {:.3f}s".format(
                rn, time.time() - t1))


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    req_queue = multiprocessing.Queue()
    req_dict = manager.dict({})
    res_dict = manager.dict({})

    service = ApiService("localhost", 5001, req_queue, req_dict, res_dict)

    predictor = Predictor(req_queue, req_dict, res_dict)
    predictor.daemon = True
    service.start()
    predictor.start()

    # time.sleep(30)
    predictor.join()
    service.join()

    # req_queue = multiprocessing.Queue()
    # res_queue = multiprocessing.Queue()

    # service = ApiService("localhost", 5001, )
    # predictor = Predictor()
    # service.run(req_queue, res_queue)
    # predictor.run(req_queue, res_queue)
