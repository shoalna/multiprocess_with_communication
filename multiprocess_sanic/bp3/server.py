from sanic import Sanic
from sanic.response import text
import random
try:
    import process
except ImportError:
    from . import process
import datetime


app = Sanic("__test_api__")


@app.get("/pre")
async def predict(request):
    print("Run sanic.predict method...")
    process.showpid()
    now = datetime.datetime.now()
    now = process.fmttime(now)
    print(f'start predict, {now}')
    app.ctx.reqd[now] = None
    print("predict Waiting response..., "
          f"reqd = {app.ctx.reqd}, resd = {app.ctx.resd}")
    while True:
        res = app.ctx.resd.get(now, None)
        if res is not None:
            break
    print(f'end predict, reqd = {app.ctx.reqd}, resd = {app.ctx.resd}')
    return text("Sanic.predict Done.")


@app.get("/enc")
async def enc(request):
    print("encing..")
    return text("Sanic.enc Done.")


@app.listener("before_server_start")
async def listener_before_server_start(*args, **kwargs):
    print("before_server_start")


@app.listener("after_server_start")
async def listener_after_server_start(*args, **kwargs):
    print("after_server_start")


@app.listener("before_server_stop")
async def listener_before_server_stop(*args, **kwargs):
    print("before_server_stop")


@app.listener("after_server_stop")
async def listener_after_server_stop(*args, **kwargs):
    print("after_server_stop")
