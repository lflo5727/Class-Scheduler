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
import numpy


def main():
    problem = Problem()
    problem.load_data()

    best_state, best_fit = simulated_annealing(problem)

    output = open("output.txt", "w")
    output.write("Fitness: {}\n".format(best_fit))
    for block in best_state:
        output.write(str(block))
        output.write("\n")
    output.close()


def simulated_annealing(problem):
    random.seed()

    # Setup temp variables
    temp = 1.0
    temp_min = 0.0001
    temp_drop = 0.95

    attempts = 0
    better_attempts = 0

    # Initialize current and best state and fitness
    current_state = random_solution(problem)
    best_state = current_state
    current_fitness = fitness_function(current_state)
    best_fit = current_fitness

    while temp > temp_min:
        # Generate a new neighbor state
        new_state = neighbor(problem, current_state)
        new_fitness = fitness_function(new_state)

        # New fit is recorded if best fit yet
        if new_fitness > best_fit:
            best_state = current_state
            best_fit = new_fitness
            better_attempts += 1

        # Assign new current state if within probability
        prob = probability(current_fitness, best_fit, temp)
        if prob > random.random():
            current_state = new_state
            current_fitness = new_fitness

        # Drop temp and reset counters
        if attempts > 4000 or better_attempts > 400:
            temp *= temp_drop
            attempts = 0
            better_attempts = 0
        attempts += 1

    return best_state, best_fit


def probability(fit_c, fit_new, tem):
    if fit_new > fit_c:
        return 1
    return numpy.exp(10000000 * (fit_new - fit_c) / tem)


def fitness_function(state):
    """Determine to cost of a state"""
    cost = 0

    rao = 0
    mit = 0
    har = 0
    bing = 0

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
            if not (block.time == other_block.time and block.room == other_block.room):
                print("Block")
                print(block.time)
                print(block.prof)
                print("Other Block")
                print(other_block.time)
                print(other_block.prof)
                print(class_time_room)
                class_time_room += 1
        cost += ((len(state) - class_time_room) * 5)

        # Room capacity is no more than twice the expected enrollment: +2
        if block.course_name.capacity * 2 <= block.room.capacity:
            cost += 2
        # For each course that does not have the same instructor teaching another course at the same time: +5
        cost += (len(state) - 1)
        for other_block in state:
            if not (other_block.time == block.time and other_block.prof == block.prof):
                cost += 5

        # Count professors' classes to teach
        if block.prof == "Rao":
            rao += 1
        if block.prof == "Mitchell":
            mit += 1
        if block.prof == "Hare":
            har += 1
        if block.prof == "Bingham":
            bing += 1
        # CS101 and CS 191 should not be scheduled for the same time -15
        if block.course_name == "101A" or block.course_name == "101B":
            for other_block in state:
                if other_block.course_name == "191A" or other_block.course_name == "191B":
                    if other_block.time == block.time:
                        cost -= 15
                    # Adjacent times +5
                    if other_block.time == block.time + 1 or other_block.time == block.time - 1:
                        cost += 5
                        # Adjacent times and same building +5, 1 in Katz -3, 1 in Bloch -3
                        if other_block.room.hall == block.room.hall:
                            cost += 5
                        if block.room.hall == "Katz" or other_block.room.hall == "Katz":
                            cost -= 3
                        if block.room.hall == "Bloch" or other_block.room.hall == "Bloch":
                            cost -= 3
        # A and B classes should be >=3 hours apart
        cost += time_apart(block, state, "101A", "101B")
        cost += time_apart(block, state, "201A", "201B")
        cost += time_apart(block, state, "191A", "191B")
        cost += time_apart(block, state, "291A", "291B")

    # For each schedule that has the same instructor teaching more than 4 courses: -5 per course over 4
    if rao > 4:
        cost -= (rao - 4) * 5
    if mit > 4:
        cost -= (mit - 4) * 5
    if har > 4:
        cost -= (har - 4) * 5
    if bing > 4:
        cost -= (bing - 4) * 5
    # For each schedule that has Rao or Mitchell teaching more courses than Hare or Bingham: -10
    if rao > har or rao > bing:
        cost -= 10
    if mit > har or mit > bing:
        cost -= 10

    return cost


def time_apart(block, state, class_a, class_b):
    if block.course_name == class_a or block.course_name == class_b:
        for other_block in state:
            if block.course_name != other_block.course_name and (
                    other_block.course_name == class_a or other_block.course_name == class_b):
                if block.time >= other_block.time + 3 or block.time <= other_block.time - 3:
                    return 5
    return 0


def neighbor(problem, previous):
    """Generate a solution that is close to the prior state"""
    new_state = previous
    ran_block = random.choice(new_state)
    item_selector = random.randint(1, 4)

    if item_selector == 1:
        ran_block.time = random.choice(problem.time_slots)
    if item_selector == 2:
        ran_block.assign_room(random.choice(problem.room_list))
    if item_selector == 3:
        while True:
            temp_pr = random.choice(problem.prof_list)
            if str(ran_block.course_name) in temp_pr.courses:
                ran_block.assign_prof(temp_pr)
                break

    return new_state


def random_solution(problem):
    """Generate a random solution to start"""
    schedule = []
    for item in problem.class_list:
        # Create block
        temp_block = ScheduleBlock(item)
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

    def convert_time(self):
        if self.time > 12:
            return "{}pm".format(self.time - 12)
        else:
            return "{}am".format(self.time)

    def __str__(self):
        return "CS {} at {} in {} with {}.".format(self.course_name, self.convert_time(), self.room, self.prof)


class Problem:
    """Problem is an object with all scheduling data, including courses and their capacities, rooms and their capacities,
    time slots, and professors and the courses they teach"""
    def __init__(self):
        self.class_list = []
        self.room_list = []
        self.prof_list = []
        self.time_slots = [10, 11, 12, 13, 14, 15, 16]

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