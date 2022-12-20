from concurrent.futures import ThreadPoolExecutor
import requests
import datetime
import time


def send():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"send {now}")
    ts = time.time()
    requests.get("http://localhost:5001/",
                 headers={'Cache-Control': 'no-cache'})
    te = time.time()
    print("Finish {:3f}".format(te - ts))
    # return r


def main():
    with ThreadPoolExecutor(max_workers=30) as executor:
        features = [executor.submit(send) for _ in range(30)]
        for _ in features:
            pass


if __name__ == "__main__":
    main()
