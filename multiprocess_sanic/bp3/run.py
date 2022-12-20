import multiprocessing
import random
import datetime
import os
try:
    import process
except ImportError:
    from . import process
from signal import SIGTERM
from server import app


class ApiService:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self._server = None
        self._loop = None
        self._process = None

        # self.req_dict = req_dict
        # self.res_dict = res_dict

    def run(self, reqd, resd):
        mp = multiprocessing.get_context("fork")
        self._process = mp.Process(
            target=self._run_server,
            args=(reqd, resd,),
            # args=(self.req_dict, self.res_dict,),
        )
        # self._process.daemon = True
        self._process.start()

    def _run_server(self, reqd, resd):
        print("Running server")
        # app.ctx.self.req_dict = self.req_dict
        # app.ctx.resd = resd
        app.ctx.reqd = reqd
        app.ctx.resd = resd
        app.run(host=self.host, port=self.port, workers=2)

    def stop(self):
        os.kill(self._process.pid, SIGTERM)
        print("Stopping server")
        self._process.join()
        self._process.terminate()


class Predictor:
    def __init__(self):
        # self.req_dict = req_dict
        # self.res_dict = res_dict
        pass

    def run(self, reqd, resd):
        print("Start run predictor, "
              f"req_dict: {reqd}, "
              f"res_dict: {resd}")

        mp = multiprocessing.get_context("fork")
        self._process = mp.Process(
            target=self.calc,
            args=(reqd, resd,),
        )
        # self._process.daemon = True
        self._process.start()

    def calc(self, reqd, resd):
        print("Running Predictor.calc")

        while True:
            if len(reqd) == 0:
                continue

            print("Predictor try get: ", list(reqd.keys())[0],
                  "from: ", reqd)
            req = list(reqd.keys())[0]
            reqd.pop(req)
            rn = random.randint(1, 3)
            process.hprocess(rn=rn)
            resd[req] = rn
            print('Predictor run rn: ', rn, resd)
            # break
            time.sleep(.1)

    def stop(self):
        os.kill(self._process.pid, SIGTERM)
        print("Stopping Predictor")
        self._process.join()
        self._process.terminate()


if __name__ == '__main__':
    import time
    with multiprocessing.Manager() as manager:
        try:
            req_dict = manager.dict({})
            res_dict = manager.dict({})

            service = ApiService("localhost", 5001, )
            service.run(req_dict, res_dict)

            predictor = Predictor()
            predictor.run(req_dict, res_dict)

            # print("Stop after 30 sec")
            # time.sleep(30)
            # predictor.stop()
            # service.stop()
            # while True:
            #     pass
        except KeyboardInterrupt:
            print("Closing server in 3 seconds")
            time.sleep(3)

            predictor.stop()
            service.stop()
