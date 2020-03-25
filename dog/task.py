import _thread
from pybricks import tools

JOIN_CHECK_INTERVAL = 10


class Task:

    def __init__(self, func, args=(), kw=None):
        self.func = func
        self.args = args
        self.kw = kw or {}
        self.lock = _thread.allocate_lock()
        self.id = None

    def start(self):
        self.lock.acquire()
        self.id = _thread.start_new_thread(self.run, ())

    def run(self):
        self.func(*self.args, **self.kw)
        self.lock.release()

    def join(self):
        while self.lock.locked():
            tools.wait(JOIN_CHECK_INTERVAL)


class TaskGroup:

    def __init__(self):
        self.tasks = []

    def add(self, func, args=(), kw=None):
        self.tasks.append(Task(func, args, kw))

    def start(self):
        for task in self.tasks:
            task.start()

    def join(self):
        for task in self.tasks:
            task.join()
