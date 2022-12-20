import random
import os

# Object that signals shutdown
_sentinel = "__STOP__"


def showpid(n_header=0):
    print(" " * n_header, "current pid: ", os.getpid())


def countdown(n=500000000, rn=None):
    print(f"Run countdown {n} - {rn}")
    showpid(4)
    while n > 0:
        if rn is None:
            rn = random.randint(1, 3)
        n -= rn
    print(f"Finish countdown {n} - {rn}")


def hprocess(rn=None):
    countdown(rn=rn)


def lprocess(rn=None):
    countdown(50000, rn=rn)


def fmttime(d):
    return d.strftime("%Y_%m_%d_%H_%M_%S_%f")
