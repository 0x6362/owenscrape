# Example 3: asynchronous requests with larger thread pool

import sys, os
import threading
import requests
from queue import Queue
import queue
from pathlib import Path

headers = {
    "user-agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"
}


def get_code(url):
    return url.split('/')[-1]

class Fetcher(object):
    def __init__(self, urls_file):
        self.urls_file = urls_file
        self.fh = open(urls_file, 'r')
        self.fetch_queue = Queue()

    def __iter__(self):
        return self

    def fill_queue(self):
        for line in self.fh.readlines():
            line = line.strip()
            if check(line):
                self.fetch_queue.put(line)
        print(self.fetch_queue.qsize(), " items added to queue")

    def __next__(self):
        if self.fetch_queue.empty():
            return None
        return self.fetch_queue.get()


def mark_failed(url):
    code = get_code(url)
    Path(f"failed/{code}").touch()

def check(url):
    code = get_code(url)
    if os.path.exists(f"failed/{code}") or os.path.exists(f"pages/{code}.html"):
        return False
    return True

class Worker(threading.Thread):
    def __init__(self, q, f, *args, **kwargs):
        self.q = q
        self.fetcher = f
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                url = self.q.get(timeout=3)  # 3s timeout
                code = get_code(url)
                r = requests.get(url.strip(), headers=headers)
                if r.status_code == requests.codes.ok:
                    with open(f"pages/{code}.html", 'wb') as f:
                        f.write(r.content)
                    print("Succeeded: ", url, r.status_code)
                else:
                    mark_failed(url)
            except queue.Empty:
                return
            self.q.task_done()

if __name__ == '__main__':
    fetcher = Fetcher("./codes.txt")
    fetcher.fill_queue()
    for _ in range(20):
        Worker(fetcher.fetch_queue, fetcher).start()

