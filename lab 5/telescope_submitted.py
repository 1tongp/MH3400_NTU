import random
import time
import math
from itertools import combinations


# this function aims to sort the L by the ending time
def sort_by_end(L):
    L.sort(key=lambda tup: tup[1])
    return L


# this function aims to sort the L by the starting time
def sort_by_start(L):
    L.sort(key=lambda tup: tup[0])
    return L


# this function aims to sort the L by the benefit
def sort_by_benefit(L):
    L.sort(key=lambda tup: tup[2], reverse=True)
    return L


# this function checks if specific combination is not conflict, False for conflict, True for not conflict
def conflict_check(lst):
    for i in range(len(lst) - 1):

        if lst[i][1] > lst[i + 1][0]:
            return False
    return True


# this function gets the possible combination of L
def combin_list(L, num):
    combination = combinations(L, num)
    combination_list = []
    for i in combination:
        combination_list.append(list(i))
    combin_copy = combination_list.copy()

    # check if the combinations are not conflict
    for i in combination_list:
        if not conflict_check(i):
            combin_copy.remove(i)

    return combin_copy


# this function checks if two tasks are conflicting. It assumes L is sorted according to starting time
def is_conflict(L):
    for i in range(len(L) - 1):
        if L[i][1] > L[i + 1][0]: return True
    return False


# this function makes a random search for assignments
def random_search(L):
    vec_assignment = [0] * len(L)

    while True:
        non_conflicting_tasks = []
        for i, el in enumerate(L):
            if vec_assignment[i] == 0:
                vec_assignment[i] = 1
                assignment = [L[k] for k in range(len(L)) if vec_assignment[k] == 1]
                if not is_conflict(assignment):
                    non_conflicting_tasks.append(i)
                vec_assignment[i] = 0

        if len(non_conflicting_tasks) == 0:
            assignment = [L[k] for k in range(len(L)) if vec_assignment[k] == 1]
            val = sum([k[2] for k in assignment])
            return (val, assignment)

        i = non_conflicting_tasks[random.randint(0, len(non_conflicting_tasks) - 1)]
        vec_assignment[i] = 1


def brute_force(L):
    sorted_l = sort_by_end(L)
    max_benefit = 0
    max_scheduling = ()

    # find the possible combination first
    for i in range(2, len(sorted_l)):
        combination_list = combin_list(sorted_l, i)
        for j in combination_list:
            benefit = 0
            for k in j:
                benefit += k[2]
            if benefit > max_benefit:
                max_benefit = benefit
                max_scheduling = j

    # if all combinations are conflict, choose the schedule with the greatest benefit
    if max_benefit == 0 and max_scheduling == ():
        for i in range(sorted_l):
            if sorted_l[2] > max_benefit:
                max_benefit = sorted_l[2]
                max_scheduling = i

    return max_benefit, max_scheduling


# this function makes a greedy force search for assignments
def greedy(L):
    sorted_l = sort_by_benefit(L)
    current = sorted_l[0]
    result = [current]
    benefit = sorted_l[0][2]

    # find the schedule with the max benefit and check if this schedule clash with the previous schedule
    for i in range(1, len(sorted_l)):
        result.append(sorted_l[i])
        result_copy = result.copy()
        result_sorted = sort_by_end(result_copy)

        # if the current schedule is not conflict with any of the previous schedules, then keep this schedule in
        # the selected list
        if conflict_check(result_sorted):
            benefit += sorted_l[i][2]

        # otherwise, remove the schedule from the selected list
        else:
            result.pop()

    result = sort_by_end(result)
    return benefit, result


# this function is to find the non conflict ancestor with the max benefit for the current element with specific index
def find_non_conflict_ancestor(accumulated_benefit, L, index):
    ancestor_list = []
    for i in range(index - 1, -1, -1):
        if L[i][1] <= L[index][0]:
            ancestor_list.append(i)

    # if there is no suitable ancestor, return -1
    if not ancestor_list:
        return -1

    # find the ancestor which has the most benefit
    max_benefit = -1
    max_benefit_ancestor = -1
    for i in range(len(ancestor_list)):
        if accumulated_benefit[ancestor_list[i]] > max_benefit:
            max_benefit = accumulated_benefit[ancestor_list[i]]
            max_benefit_ancestor = ancestor_list[i]
    return max_benefit_ancestor


# this function makes a dynamic programing search for assignments
def dynamic_prog(L):
    # sorted L by its ending time
    sorted_l = sort_by_end(L)

    # As the first element in the L does not have an ancestor, so we record the -1 instead
    ancestor_index = [-1] * len(sorted_l)

    # this array records the accumulated benefit from the ancestor to the current schedule
    accumulated_benefit = [0] * len(sorted_l)
    accumulated_benefit[0] = sorted_l[0][2]

    # find the non conflict the latest ancestor of each schedule, and update the accumulated benefit
    for i in range(1, len(sorted_l)):
        ancestor = find_non_conflict_ancestor(accumulated_benefit, L, i)

        # if the current schedule has a non conflict ancestor, then calculate the accumulated benefit
        if ancestor != -1:
            ancestor_index[i] = ancestor
            current_benefit = accumulated_benefit[ancestor]
            current_benefit += sorted_l[i][2]

        # otherwise
        else:
            current_benefit = sorted_l[i][2]

        # update the accumulated benefit array
        accumulated_benefit[i] = current_benefit

    # find the max benefit index from the accumulated benefit array
    max_benefit = -1
    max_benefit_index = -1
    for i in range(len(sorted_l)):
        if accumulated_benefit[i] > max_benefit:
            max_benefit = accumulated_benefit[i]
            max_benefit_index = i

    # find the composite which has the greatest benefit
    result = [sorted_l[max_benefit_index]]
    while True:
        if ancestor_index[max_benefit_index] == -1:
            return max_benefit, result
        else:
            early_ancestor = ancestor_index[max_benefit_index]
            result.append(sorted_l[early_ancestor])
            max_benefit_index = early_ancestor
            result = sort_by_end(result)


# this function prints the taskes
def print_tasks(L):
    for i, t in enumerate(L):
        print("task %2i (b=%2i):" % (i, t[2]), end="")
        print(" " * round(t[0] / 10) + "-" * round((t[1] - t[0]) / 10))


# this function tests and times a telescope tasks assignment search
def test_telescope(algo, my_tab, display):
    tab = my_tab.copy()
    print("testing", algo, str(" " * (14 - len(algo))), "... ", end='')
    t = time.time()
    (max_temp, assignment_temp) = eval(algo + "(tab)")
    print("done ! It took {:.2f} seconds".format(time.time() - t))
    if max_temp != None:
        print("Solution with benefit = %i" % (max_temp), end='\n')
    if display:
        if assignment_temp != None:
            print_tasks(assignment_temp)
            print()


MAX_BENEFIT = 99
MAX_START_TIME = 500
MAX_DURATION = 250

NUMBER_OF_ELEMENTS = 10
print("\n ******** Testing to solve for %i events ********" % (NUMBER_OF_ELEMENTS))
val = [(random.randint(1, MAX_START_TIME), random.randint(1, MAX_DURATION), random.randint(1, MAX_BENEFIT)) for i in
       range(NUMBER_OF_ELEMENTS)]
tab = sorted([(val[i][0], val[i][0] + val[i][1], val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
print("Problem instance: ")
print_tasks(tab)
print("")
test_telescope("random_search", tab, True)
test_telescope("brute_force", tab, True)
test_telescope("greedy", tab, True)
test_telescope("dynamic_prog", tab, True)

NUMBER_OF_ELEMENTS = 20
print("\n ******** Testing to solve for %i events ********" % (NUMBER_OF_ELEMENTS))
val = [(random.randint(1, MAX_START_TIME), random.randint(1, MAX_DURATION), random.randint(1, MAX_BENEFIT)) for i in
       range(NUMBER_OF_ELEMENTS)]
tab = sorted([(val[i][0], val[i][0] + val[i][1], val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
test_telescope("random_search", tab, False)
test_telescope("brute_force", tab, False)
test_telescope("greedy", tab, False)
test_telescope("dynamic_prog", tab, False)

# Algorithms are fun!
