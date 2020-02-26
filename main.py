###############################################################
#
#                       Liam Floyd
#                        CS 461
#                       Program 2
#
###############################################################
import prof
import room
import course
import random


def main():
    problem = Problem()
    problem.load_data()


    simulated_annealing(problem)


def simulated_annealing(problem):
    random.seed()

    temp_max = 1
    temp_min = 0.0001

    temp_drop = 0.95
    attempts_to_drop = 400

    inital_state = random_solution(problem)
    best_state = inital_state

def cost_function(problem, state):
    cost = 0

    for block in state:
        # For each course that is taught by an instructor who can teach it, other than Staff: +3
        if str(block.prof) != "Staff":
            cost += 3
        # For each course taught by Staff: +1
        else:
            cost += 1
        # For each course that is the only course scheduled in that room at that time: +5
        class_time_room = -1
        for other_block in state:
            if block.time == other_block.time and block.room == other_block.room:
                class_time_room += 1
        cost += ((len(state) - class_time_room) * 5)

        # Room capacity is no more than twice the expected enrollment: +2


        # For each course that does not have the same instructor teaching another course at the same time: +5
        cost += (len(state) - 1)

        # For each schedule that has the same instructor teaching more than 4 courses: -5 per course over 4

        # For each schedule that has Rao or Mitchell (graduate faculty) teaching more courses than Hare or Bingham (same number of courses is OK): -10

        # CS101 and CS 191 should not be scheduled for the same time -15
        if block.course_name == "101A" or block.course_name == "101B":
            for other_block in state:
                if other_block.course_name == "191A" or other_block.course_name == "191B":
                    if other_block.time == block.time:
                        cost -= 15
                    if other_block.time == block.time + 1 or other_block.time == block.time - 1:
                        cost += 5
                        if other_block.room.hall == block.room.hall:
                            cost += 5
                        if block.room.hall == "Katz" or other_block.room.hall == "Katz":
                            cost -= 3
                        if block.room.hall == "Bloch" or other_block.room.hall == "Bloch":
                            cost -= 3
        # Adjacent times +5
        # Adjacent times and same building +5, 1 in Katz -3, 1 in Bloch -3
        # A and B classes should be >=3 hours apart




def random_solution(problem):
    """Generate a random solution to start"""
    schedule = []
    for item in problem.class_list:
        # Create block
        temp_block = ScheduleBlock(item.name)
        # assign prof
        while True:
            temp_pr = random.choice(problem.prof_list)
            if item.name in temp_pr.courses:
                temp_block.assign_prof(temp_pr)
                break
        # assign room
        while True:
            temp_rm = random.choice(problem.room_list)
            if item.capacity <= temp_rm.capacity:
                temp_block.assign_room(temp_rm)
                break
        # assign time
        while True:
            temp_tm = random.choice(problem.time_slots)
            if len(schedule) == 0:
                temp_block.assign_time(temp_tm)
                break
            cnt = 0
            for prior in schedule:
                if prior.time == temp_tm and prior.prof == temp_block.prof:
                    cnt += 1
            if cnt == 0:
                temp_block.assign_time(temp_tm)
                break

        schedule.append(temp_block)
        print(str(temp_block))

    return schedule


class ScheduleBlock:
    """A block in the schedule including all final info for a session"""
    def __init__(self, name):
        self.course_name = name
        self.time = 0
        self.prof = "TBD"
        self.room = "TBD"

    def assign_time(self, time):
        self.time = time

    def assign_prof(self, inst):
        self.prof = inst

    def assign_room(self, loc):
        self.room = loc

    def __str__(self):
        return "CS {} at {} in {} with {}.".format(self.course_name, self.time, self.room, self.prof)


class Problem:
    """Problem is an object with all scheduling data, including courses and their capacities, rooms and their capacities,
    time slots, and professors and the courses they teach"""
    def __init__(self):
        self.class_list = []
        self.room_list = []
        self.prof_list = []
        self.time_slots = [10, 11, 12, 1, 2, 3, 4]

    def load_data(self):
        """Load the data from the file to populate lists"""
        file = open("data.txt", "r")

        for line in file:
            values = line.split()
            if values[0] == "cs":
                temp_class = course.Course(values[1], values[2])
                self.class_list.append(temp_class)
                # print(temp_class)
            if values[0] == "rm":
                temp_room = room.Room(values[1], values[2], values[3])
                self.room_list.append(temp_room)
                # print(temp_room)
            if values[0] == "pf":
                temp_prof = prof.Prof(values[1])
                for subject in values[2:]:
                    temp_prof.add_course(subject)
                self.prof_list.append(temp_prof)
                # print(temp_prof)


if __name__ == "__main__":
    main()