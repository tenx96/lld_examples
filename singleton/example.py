import threading


class SingletonFactory:
    _instance = None
    _lock = threading.Lock()

    def foo(self):
        print("bar")

    def __new__(cls):
        if not cls._instance:
            # creation step
            with cls._lock:
                if not cls._instance:
                    print("Creating class instance")
                    cls._instance = super().__new__(cls)

        return cls._instance


ins1 = SingletonFactory()
ins2 = SingletonFactory()
ins3 = SingletonFactory()

assert ins1 is ins2 is ins3

ins1.foo()
