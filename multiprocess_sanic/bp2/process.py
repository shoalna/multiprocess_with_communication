import random


def countdown(n=5000000, rn=None):
    print(f"Run countdown {n} - {rn}")
    while n > 0:
        if rn is None:
            rn = random.randint(1, 10)
        n -= rn
    print(f"Finish countdown {n} - {rn}")


def hprocess(rn=None):
    countdown(rn=rn)


def lprocess(rn=None):
    countdown(50000, rn=rn)
