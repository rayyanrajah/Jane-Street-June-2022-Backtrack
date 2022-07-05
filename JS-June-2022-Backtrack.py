# Jane Street June 2022 puzzle solution
# Link to puzzle: https://www.janestreet.com/puzzles/archive/
# NOTE: Despite the additional logic, the program still takes a while to compute the answer.
# A resolution for this, which I am currently working on, would be to model the problem as a linear program and use the Python PuLP library to solve it.
# Similar Sudoku LP https://github.com/rayyanrajah/Sudoku-Linear-Programming

import numpy as np
import itertools
import re
import time

start = time.time()

# list of jagged matrices i.e. regions of puzzle board
j = [[0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
     [3, 0, 0, 0, 4, 0],
     [0, 7, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0],
     [0, 0, 1],
     [0, 0],
     [0, 0, 0, 0, 0, 0],
     [2, 0, 0, 0, 0, 0, 6],
     [0, 0, 1, 0],
     [0, 0, 0],
     [0, 0],
     [0],
     [0],
     [0, 0, 0, 0, 0],
     [0],
     [0, 3, 2],
     [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
     [0, 0],
     [0, 0, 0],
     [0, 0, 0, 5, 0],
     [0],
     [0, 0, 0, 6, 0, 0, 0, 2, 0],
     [0, 0, 0, 0]]

# string form of where elements of jagged matrices will be on a cartesian grid
string_grid = [["j[0][0]", "j[1][0]", "j[1][1]", "j[1][2]", "j[2][0]", "j[2][1]", "j[2][2]", "j[2][3]", "j[2][4]", "j[2][5]"],
               ["j[0][1]", "j[0][2]", "j[1][3]", "j[1][4]", "j[1][5]", "j[2][6]", "j[3][0]", "j[3][1]", "j[2][7]", "j[2][8]"],
               ["j[0][3]", "j[0][4]", "j[4][0]", "j[4][1]", "j[5][0]", "j[5][1]", "j[6][0]", "j[3][2]", "j[7][0]", "j[7][1]"],
               ["j[0][5]", "j[0][6]", "j[8][0]", "j[4][2]", "j[9][0]", "j[6][1]", "j[6][2]", "j[6][3]", "j[7][2]", "j[7][3]"],
               ["j[0][7]", "j[8][1]", "j[8][2]", "j[9][1]", "j[9][2]", "j[10][0]", "j[11][0]", "j[6][4]", "j[6][5]", "j[7][4]"],
               ["j[0][8]", "j[12][0]", "j[8][3]", "j[13][0]", "j[14][0]", "j[10][1]", "j[15][0]", "j[15][1]", "j[7][5]", "j[7][6]"],
               ["j[0][9]", "j[16][0]", "j[17][0]", "j[13][1]", "j[13][2]", "j[13][3]", "j[15][2]", "j[18][0]", "j[18][1]", "j[18][2]"],
               ["j[16][1]", "j[16][2]", "j[17][1]", "j[19][0]", "j[13][4]", "j[20][0]", "j[21][0]", "j[22][0]", "j[22][1]", "j[21][1]"],
               ["j[16][3]", "j[16][4]", "j[16][5]", "j[19][1]", "j[19][2]", "j[21][2]", "j[21][3]", "j[22][2]", "j[22][3]", "j[21][4]"],
               ["j[16][6]", "j[16][7]", "j[16][8]", "j[16][9]", "j[19][3]", "j[19][4]", "j[21][5]", "j[21][6]", "j[21][7]", "j[21][8]"]]

# grid of cartesian coordinates
c_grid = list(itertools.product(range(10), repeat=2))

# grid of jagged coordinates
j_grid = [tuple(map(int, re.findall(r"\d+", string_grid[i][k]))) for i in range(10) for k in range(10)]

print(j_grid)

class mappings:
    def __init__(self, cc, jc):
        self.cc = cc
        self.jc = jc

    # for converting cartesian coordinates to jagged coordinates
    def c_to_j_map(self):
        tmp = {}
        for i in range(100):
            tmp[self.cc[i]] = self.jc[i]
        return tmp

    # for converting jagged coordinates to cartesian coordinates
    def j_to_c_map(self):
        tmp = {}
        for i in range(100):
            tmp[self.jc[i]] = self.cc[i]
        return tmp

    # groups together cartesian coordinates of elements in the same jagged matrix
    def in_same_jagged(self):
        tmp1 = {}
        for i in range(len(j)):
            tmp1[i] = []
        for key in self.j_to_c_map().keys():
            tmp1[key[0]].append(self.j_to_c_map()[key])
        return tmp1


maps = mappings(c_grid, j_grid)

print(maps.in_same_jagged())

# list of possible elements at each cartesian coordinate
p_grid = {}
for i in c_grid:
    p_grid[(i[0], i[1])] = []

# number grid (the puzzle board)
grid = []
for i in range(10):
    grid.append([])
    for k in range(10):
        grid[i].append(eval(string_grid[i][k]))


# checks if it's possible for n to be placed at (y, x) on the grid
def possible(y, x, n):
    j_indexes = [index for index in maps.c_to_j_map()[(y, x)]]

    # check if n is larger than the size of the jagged matrix
    if n > len(j[j_indexes[0]]):
        return False

    # check if n is already an element of jagged matrix
    for i in range(len(j[j_indexes[0]])):
        if n == j[j_indexes[0]][i]:
            return False

    # check if the nearest n via taxicab distance is less than n cells away
    for i in range(n):
        for k in range(2 * i + 1):
            if 0 <= y + n - 1 - i <= 9 and 0 <= x - i + k <= 9:
                if n == grid[y + n - 1 - i][x - i + k]:
                    return False
            if 0 <= y - n + 1 + i <= 9 and 0 <= x - i + k <= 9:
                if n == grid[y - n + 1 + i][x - i + k]:
                    return False
    return True


# populates the p_grid
# p_grid is the list of possible elements at each cartesian coordinate
def add_possibilities():
    for y in range(10):
        for x in range(10):
            if grid[y][x] == 0:
                for n in range(1, 11):
                    if possible(y, x, n):
                        p_grid[(y, x)].append(n)


add_possibilities()


# updates p_grid
# p_grid is the list of possible elements at each cartesian coordinate
def update(y, x, n):
    j_indexes = [index for index in maps.c_to_j_map()[(y, x)]]

    # place n at (y, x) and update the jagged matrix n belongs to
    j[j_indexes[0]][j_indexes[1]] = n
    grid[y][x] = n

    # remove all elements from p_grid[(y, x)] since n has been placed at (y, x)
    p_grid[(y, x)] = []

    # remove n as a possibility from all cells less than n distance away
    for i in range(n):
        for k in range(2 * i + 1):
            if 0 <= y + n - 1 - i <= 9 and 0 <= x - i + k <= 9 and n in p_grid[(y + n - 1 - i, x - i + k)]:
                p_grid[(y + n - 1 - i, x - i + k)].remove(n)
            if 0 <= y - n + 1 + i <= 9 and 0 <= x - i + k <= 9 and n in p_grid[(y - n + 1 + i, x - i + k)]:
                p_grid[(y - n + 1 + i, x - i + k)].remove(n)

    # remove n as a possibility from all cells in same jagged matrix as n
    for i in maps.in_same_jagged()[j_indexes[0]]:
        if n in p_grid[i]:
            p_grid[i].remove(n)

    return


# if there is only one possible element that can be placed at (y, x),
# then place that element at (y, x)
def one_possibility():
    for key in p_grid.keys():
        if len(p_grid[key]) == 1:
            y = key[0]
            x = key[1]
            n = p_grid[key][0]
            update(y, x, n)
            return True
    return False


# if a number that is missing from the jagged matrix can only be placed at (y, x),
# then place that element at (y, x)
def reverse_one():
    list1 = []
    list2 = []
    for i in range(len(j)):
        list1.append([])
        list2.append([])
        for k in range(len(j[i])):
            list2[i].append([])
            for m in range(len(p_grid[maps.in_same_jagged()[i][k]])):
                list1[i].append(p_grid[maps.in_same_jagged()[i][k]][m])
                list2[i][k].append(p_grid[maps.in_same_jagged()[i][k]][m])
    f = 0
    p = 0
    for i in range(len(list1)):
        for n in range(1, 11):
            if list1[i].count(n) == 1:
                f = n
                p = i
                break
        else:
            continue

    for i in range(len(list2[p])):
        if f in list2[p][i]:
            y = maps.j_to_c_map()[(p, i)][0]
            x = maps.j_to_c_map()[(p, i)][1]
            n = f
            update(y, x, n)
            return True
    return False


# for n at (y, x), checks if there exists n that is n distance away from n
# "checks if n has a neighbour"
def neighbour_search(y, x, n):
    for i in range(n + 1):
        if 0 <= y + n - i <= 9 and 0 <= x + i <= 9:
            if grid[y + n - i][x + i] == n:
                return True
        if 0 <= y + n - i <= 9 and 0 <= x - i <= 9:
            if grid[y + n - i][x - i] == n:
                return True
    for i in range(n):
        if 0 <= y - n + i <= 9 and 0 <= x + i <= 9:
            if grid[y - n + i][x + i] == n:
                return True
        if 0 <= y - n + i <= 9 and 0 <= x - i <= 9:
            if grid[y - n + i][x - i] == n:
                return True
    return False


# if n has no neighbours and only one space that is n taxicab distance away is empty,
# then place n in that empty space
def neighbour_solve():
    for y in range(10):
        for x in range(10):
            if grid[y][x] != 0 and not neighbour_search(y, x, grid[y][x]):
                n = grid[y][x]
                counter = 0
                for i in range(n + 1):
                    if i == 0:
                        if 0 <= y + n <= 9 and 0 <= x <= 9:
                            if grid[y + n][x] == 0 and n in p_grid[(y + n, x)]:
                                counter += 1
                    else:
                        if 0 <= y + n - i <= 9 and 0 <= x + i <= 9:
                            if grid[y + n - i][x + i] == 0 and n in p_grid[(y + n - i, x + i)]:
                                counter += 1
                        if 0 <= y + n - i <= 9 and 0 <= x - i <= 9:
                            if grid[y + n - i][x - i] == 0 and n in p_grid[(y + n - i, x - i)]:
                                counter += 1
                for i in range(n):
                    if i == 0:
                        if 0 <= y - n <= 9 and 0 <= x <= 9:
                            if grid[y - n][x] == 0 and n in p_grid[(y - n, x)]:
                                counter += 1
                    else:
                        if 0 <= y - n + i <= 9 and 0 <= x + i <= 9:
                            if grid[y - n + i][x + i] == 0 and n in p_grid[(y - n + i, x + i)]:
                                counter += 1
                        if 0 <= y - n + i <= 9 and 0 <= x - i <= 9:
                            if grid[y - n + i][x - i] == 0 and n in p_grid[(y - n + i, x - i)]:
                                counter += 1

                if counter == 1:
                    for i in range(n + 1):
                        if 0 <= y + n - i <= 9 and 0 <= x + i <= 9:
                            if grid[y + n - i][x + i] == 0 and n in p_grid[(y + n - i, x + i)]:
                                y = y + n - i
                                x = x + i
                                update(y, x, n)
                                return True
                        if 0 <= y + n - i <= 9 and 0 <= x - i <= 9:
                            if grid[y + n - i][x - i] == 0 and n in p_grid[(y + n - i, x - i)]:
                                y = y + n - i
                                x = x - i
                                update(y, x, n)
                                return True
                    for i in range(n):
                        if 0 <= y - n + i <= 9 and 0 <= x + i <= 9:
                            if grid[y - n + i][x + i] == 0 and n in p_grid[(y - n + i, x + i)]:
                                y = y - n + i
                                x = x + i
                                update(y, x, n)
                                return True
                        if 0 <= y - n + i <= 9 and 0 <= x - i <= 9:
                            if grid[y - n + i][x - i] == 0 and n in p_grid[(y - n + i, x - i)]:
                                y = y - n + i
                                x = x - i
                                update(y, x, n)
                                return True
    return False


# backtracking algorithm to solve grid
def backtrack():
    for y in range(10):
        for x in range(10):
            j_indexes = [index for index in maps.c_to_j_map()[(y, x)]]
            if grid[y][x] == 0:
                for n in range(1, 11):
                    if possible(y, x, n):
                        j[j_indexes[0]][j_indexes[1]] = n
                        grid[y][x] = n
                        backtrack()
                        j[j_indexes[0]][j_indexes[1]] = 0
                        grid[y][x] = 0
                return
    print(np.matrix(grid))


# computes the product of the values in each row, and then takes the sum of these products
def sum_of_product_of_rows():
    total_sum = 0
    for y in range(10):
        tmp_sum = 1
        for x in range(10):
            tmp_sum *= grid[y][x]
        total_sum += tmp_sum
    print(f"\nSum of the product of the values in each row: {total_sum}")
    return


# recursive function to solve grid
def solve():
    if one_possibility():
        solve()
    elif reverse_one():
        solve()
    elif neighbour_solve():
        solve()
    else:
        backtrack()


solve()

sum_of_product_of_rows()

# prints runtime of program
end = time.time()
print(f"\nRuntime: {end - start}")
