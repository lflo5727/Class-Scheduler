class Prof:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def __str__(self):
        return "{}".format(self.name)