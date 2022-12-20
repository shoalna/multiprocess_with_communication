import multiprocessing
import random
import datetime
try:
    import process
except ImportError:
    from . import process


def fmttime(d):
    return d.strftime("%Y_%m_%d_%H_%M_%S_%f")


def w1(reqd: dict, resd: dict):
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


def w2(reqd: dict, resd: dict):
    print('start worker2')
    while True:
        if len(reqd) == 0:
            continue
        print("worker2 try get: ", list(req_dict.keys())[0], "from: ", reqd)
        req = list(req_dict.keys())[0]
        reqd.pop(req)
        rn = random.randint(1, 10)
        process.hprocess(rn=rn)
        resd[req] = rn
        print('worker2 use rn: ', rn, resd)
        break
    print('end worker2')


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        req_dict = manager.dict({})
        res_dict = manager.dict({})

        p1 = multiprocessing.Process(target=w1, args=(req_dict, res_dict,))
        p2 = multiprocessing.Process(target=w2, args=(req_dict, res_dict,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()
