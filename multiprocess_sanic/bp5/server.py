from sanic import Sanic
from sanic.response import text
import asyncio
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
    app.ctx.req_queue.put(now)
    app.ctx.req_dict[now] = None
    print("predict Waiting response..., ")
    while True:
        # res = app.ctx.resq.get(now, None)
        if now in app.ctx.res_dict:
            res = app.ctx.res_dict.pop(now)
            break
        await asyncio.sleep(.5)
    print(f'end predict, got result = {res}, '
          f'expect = {now}, '
          f'response queue = {app.ctx.res_dict}')
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
    app.ctx.req_queue.put(process._sentinel)


@app.listener("after_server_stop")
async def listener_after_server_stop(*args, **kwargs):
    print("after_server_stop")
