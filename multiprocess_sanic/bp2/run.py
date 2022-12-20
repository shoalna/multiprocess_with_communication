import multiprocessing
import random
import datetime
import time
try:
    import process
except ImportError:
    from . import process
import os
from signal import SIGTERM


def fmttime(d):
    return d.strftime("%Y_%m_%d_%H_%M_%S_%f")


class ApiService:
    def __init__(self) -> None:
        pass

    def run(self, reqd, resd):
        mp = multiprocessing.get_context("fork")
        self._process = mp.Process(
            target=self.w1,
            args=(reqd, resd,),
            # args=(self.req_dict, self.res_dict,),
        )
        self._process.daemon = True
        self._process.start()

    def w1(self, reqd: dict, resd: dict):
        now = datetime.datetime.now()
        now = fmttime(now)
        print(f'start worker1, {now}')
        reqd[now] = None
        print(f"worker1 Waiting response..., reqd = {reqd}, resd = {resd}")
        while True:
            res = resd.get(now, None)
            if res is not None:
                break
        print(f'end worker1, reqd = {reqd}, resd = {resd}')

    def stop(self):
        print(f"Stopping ApiService: {self._process.pid}")
        os.kill(self._process.pid, SIGTERM)
        self._process.join()
        self._process.terminate()


class Predictor:
    def __init__(self) -> None:
        pass

    def run(self, reqd, resd):
        mp = multiprocessing.get_context("fork")
        self._process = mp.Process(
            target=self.w2,
            args=(reqd, resd,),
            # args=(self.req_dict, self.res_dict,),
        )
        self._process.daemon = True
        self._process.start()

    def w2(self, reqd: dict, resd: dict):
        print('start worker2')
        print('worker2 Waiting request...')
        while True:
            if len(reqd) == 0:
                continue
            print("worker2 try get: ", list(req_dict.keys())[0],
                  "from: ", reqd)
            req = list(req_dict.keys())[0]
            reqd.pop(req)
            rn = random.randint(1, 10)
            process.hprocess(rn=rn)
            resd[req] = rn
            print('worker2 use rn: ', rn, resd)
            # break
        # print('end worker2')

    def stop(self):
        print(f"Stopping Predictor: {self._process.pid}")
        os.kill(self._process.pid, SIGTERM)
        self._process.join()
        self._process.terminate()


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        try:
            req_dict = manager.dict({})
            res_dict = manager.dict({})

            service = ApiService()
            service.run(req_dict, res_dict)

            predictor = Predictor()
            predictor.run(req_dict, res_dict)

            print("Stop after 10 sec")
            time.sleep(10)
            predictor.stop()
            service.stop()

        except KeyboardInterrupt:
            predictor.stop()
            service.stop()
            # raise
