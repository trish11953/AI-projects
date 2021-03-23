############################################################
# CMPSC442: Homework 7
############################################################

student_name = "Trisha Mandal"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    return [(a, b) for a in range(0, 9) for b in range(0, 9)]


def sudoku_arcs():
    resultarcs = []

    for x in sudoku_cells():
        for y in sudoku_cells():
            currentx = x[0]
            currenty = y[0]
            nextx = x[1]
            nexty = y[1]

            if x != y and nextx == nexty:
                resultarcs.append((x, y))

            elif x != y and currentx == currenty:
                resultarcs.append((x, y))

            elif x != y and currentx // 3 == currenty // 3 and nextx // 3 == nexty // 3:
                resultarcs.append((x, y))
    return resultarcs


def read_board(path):
    read = {}
    loc = open(path)
    with loc as f:
        a = 0
        for thread in f:
            b = 0
            for text in thread:
                read[(a, b)] = {ord(text) - 48} if text != "*" else {1, 2, 3, 4, 5, 6, 7, 8, 9}
                b = b + 1
            a = a + 1
    return read


class Sudoku(object):

    maxSet = {i for i in range(1, 10)}
    sudokucells, sudokuarcs  = sudoku_cells(), sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        c1 = self.board[cell1]
        c2 = self.board[cell2]
        l = len(c2)
        itera = next(iter(c2))

        if l == 1 and itera in c1:
            self.board[cell1] = self.board[cell1] - self.board[cell2]
            return True
        elif l != 1 and itera not in c1:
            return False

    def infer_ac3(self):
        flag, alteredcells = False, self.sudokucells

        while len(alteredcells) != 0:
            newcells = []

            for cellaltered, updatecell in self.sudokuarcs:
                p1 = cellaltered in alteredcells
                p2 = self.remove_inconsistent_values(updatecell, cellaltered)
                if p1 and p2:
                    flag = True
                    if updatecell not in newcells:
                        newcells.append(updatecell)
            alteredcells = newcells
        return flag

    def get_Union(self, cellSet):
        sumunion = set([])
        for cell in cellSet:
            sumunion = sumunion.union(self.board[cell])
        return sumunion

    def infer_improved(self):
        stopped, flag = False, False

        while not stopped:
            allCELLS, originalb, success = Sudoku.sudokucells, copy.deepcopy(self.board), Sudoku.infer_ac3(self)

            if not success:
                return False

            for cell in allCELLS:
                if len(self.board[cell]) > 1:
                    i, j, arcs = cell[0], cell[1], 0

                    rowcells = set([(i, t) for t in range(9) if j != t])
                    row_union = self.get_Union(rowcells)
                    columncells = set([(t, j) for t in range(9) if i != t])
                    column_union = self.get_Union(columncells)

                    if i < 3 and j < 3:
                        arcs = set([(a, b) for a in range(3) for b in range(3) if j != b or i != a])
                    elif i < 3 and j < 6:
                        arcs = set([(a, b) for a in range(3) for b in range(3, 6) if j != b or i != a])
                    elif i < 3 and not j < 3 and not j < 6:
                        arcs = set([(a, b) for a in range(3) for b in range(6, 9) if j != b or i != a])
                    elif i < 6 and j < 3:
                        arcs = set([(a, b) for a in range(3, 6) for b in range(3) if j != b or i != a])
                    elif i < 6 and j < 6:
                        arcs = set([(a, b) for a in range(3, 6) for b in range(3, 6) if j != b or i != a])
                    elif i < 6 and not j < 3 and not j < 6:
                        arcs = set([(a, b) for a in range(3, 6) for b in range(6, 9) if j != b or i != a])
                    elif not i < 3 and not i < 6 and j < 3:
                        arcs = set([(a, b) for a in range(6, 9) for b in range(3) if j != b or i != a])
                    elif not i < 3 and not i < 6 and j < 6:
                        arcs = set([(a, b) for a in range(6, 9) for b in range(3, 6) if j != b or i != a])
                    elif not i < 3 and not i < 6 and not j < 3 and not j < 6:
                        arcs = set([(a, b) for a in range(6, 9) for b in range(6, 9) if j != b or i != a])

                    boxUnion = self.get_Union(arcs)

                    intersect = row_union.intersection(column_union)
                    intersect = intersect.intersection(boxUnion)
                    diff = self.maxSet - intersect
                    if len(diff) == 1:
                        self.board[cell] = diff

            if originalb == self.board:
                stopped = True
        return False if not flag else True

    def is_solved(self):
        return [False for j in range(0, 9) for i in range(0, 9) if len(self.board[(i, j)]) != 1]

    def infer_with_guessing(self):

        self.infer_improved()

        current = self.board
        retrace = copy.deepcopy(current)

        for currentcell in self.sudokucells:

            l = len(current[currentcell])

            if l == 1:
                continue
            elif l != 1:
                break

            for item in current[currentcell]:

                current[currentcell].add(item)

                if self.is_solved():
                    return True

                current = retrace

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Took me 16 hours to complete this project 
"""

feedback_question_2 = """
Understanding infer_improved() and infer_with_guessing() was hard and it took me a while to code. 
"""

feedback_question_3 = """
The concept seems to be fun but some of the functions in the assignment pdf was not well explained.
"""

