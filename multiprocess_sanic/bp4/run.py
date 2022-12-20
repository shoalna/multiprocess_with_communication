import queue
import socket
import os

import select
import multiprocessing
import threading
import time


class PollableQueue(queue.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a pair of connected sockets
        if os.name == 'posix':
            self._putsocket, self._getsocket = socket.socketpair()
        else:
            # Compatibility on non-POSIX systems
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self._putsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._putsocket.connect(server.getsockname())
            self._getsocket, _ = server.accept()
            server.close()

    def fileno(self):
        return self._getsocket.fileno()

    def put(self, item):
        super().put(item)
        self._putsocket.send(b'x')

    def get(self):
        self._getsocket.recv(1)
        return super().get()

    # def __str__(self) -> str:
    #     print(", ".join(list(self.queue)))
    #     return "<PollableQueue: [" + ", ".join(list(self.queue)) + "]>"


def consumer(queues):
    '''
    Consumer that reads data on multiple queues simultaneously
    '''
    while True:
        can_read, _, _ = select.select(queues, [], [])
        for r in can_read:
            item = r.get()
            print('Got:', item)


def creater(queues):
    q1, q2, q3 = queues
    # Feed data to the queues
    q1.put(1)
    q2.put(10)
    q3.put('hello')
    q2.put(15)
    q2.put(9999)
    print(f"creater done, {q1}, {q2}, {q3}")


if __name__ == '__main__':
    q1 = PollableQueue()
    q2 = PollableQueue()
    q3 = PollableQueue()
    t = multiprocessing.Process(target=creater, args=([q1, q2, q3],))
    t2 = multiprocessing.Process(target=consumer, args=([q1, q2, q3],))
    # t = threading.Thread(target=creater, args=([q1, q2, q3],))
    # t2 = threading.Thread(target=consumer, args=([q1, q2, q3],))
    # t.daemon = True
    # t.daemon = True
    t.start()
    t2.start()

    # Give thread time to run
    time.sleep(1)
    t.join()
    t2.join()
