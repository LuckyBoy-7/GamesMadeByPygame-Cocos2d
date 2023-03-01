class Stats(object):
    LOW, MIDDLE, HIGH = range(3)

    def __init__(self):
        self.level = Stats.LOW

        self.first_click = True
        self.running = True


stats = Stats()
