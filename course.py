class Course:
    def __init__(self, name, cap):
        self.name = name
        self.capacity = cap

    def __str__(self):
        return "CS {} ({})".format(self.name, self.capacity)
