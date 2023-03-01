class Timer(object):
    def __init__(self, time: int, elapse: int = 0, condition: bool = None):
        self.time = time
        self.elapse = elapse
        self.condition = condition

    def on_time(self):
        if self.condition is None or self.condition:
            self.elapse += 1

        if self.elapse > self.time:
            self.elapse = 0
            self.condition = False if self.condition is not None else None
            return True
        return False
