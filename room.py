class Room:
    def __init__(self, hall, number, cap):
        self.hall = hall
        self.number = number
        self.capacity = cap

    def __str__(self):
        return "{} {}".format(self.hall, self.number)