class Task:
    def __init__(self, nr, time):
        self.nr = nr # task number readed from file
        self.time = time # list with each job time
        self.priority = sum(self.time)
