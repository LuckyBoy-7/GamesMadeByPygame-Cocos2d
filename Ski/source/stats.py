class Stats(object):
    WELCOME, START = range(2)

    def __init__(self):
        self.state = self.WELCOME
        self.score = 0


stats = Stats()