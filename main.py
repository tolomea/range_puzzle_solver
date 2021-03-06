from __future__ import print_function, unicode_literals, absolute_import, division

from collections import defaultdict


example = """
....14......
08..........
..........04
............
..02....10..
............
04..........
..........07
......07....
"""


def parse(data):
    numbers = {}
    row = 0
    column = 0
    for line in data.splitlines():
        line = line.strip()
        if line:
            column = 0
            for i in range(0, len(line), 2):
                cell = line[i:i + 2]
                try:
                    number = int(cell)
                except ValueError:
                    pass
                else:
                    numbers[(row, column)] = number
                column += 1
            row += 1
    return row, column, numbers


def cross(row, column, number):
    patterns = []
    for n in range(number):
        for e in range(number - n):
            for s in range(number - n - e):
                w = number - n - e - s - 1

                empty = set()
                blocked = set()

                for i in range(1, n + 1):
                    empty.add((row - i, column))
                for i in range(1, e + 1):
                    empty.add((row, column + i))
                for i in range(1, s + 1):
                    empty.add((row + i, column))
                for i in range(1, w + 1):
                    empty.add((row, column - i))
                blocked.update([
                    (row - n - 1, column),
                    (row, column + e + 1),
                    (row + s + 1, column),
                    (row, column - w - 1),
                ])

                patterns.append((empty, blocked))
    return patterns


class Pattern(object):
    def __init__(self, row, column, empty, blocked):
        self.cell = (row, column)
        # True = blocked, False = empty, None = unknown
        self.blocked_cells = {}
        for c in empty:
            self.blocked_cells[c] = False
        for c in blocked:
            self.blocked_cells[c] = True
        self.eliminated = False


class State(object):
    def __init__(self, data):
        self.height, self.width, self.numbers = parse(data)
        self.patterns_for_cell = defaultdict(list)
        self.patterns_for_empty_cell = defaultdict(list)
        self.patterns_for_blocked_cell = defaultdict(list)
        self.empty_cells = set()
        self.blocked_cells = set()
        self.unknown_cells = {(r, c) for r in range(self.height) for c in range(self.width)}

        for (row, column), number in self.numbers.iteritems():
            for empty, blocked in cross(row, column, number):
                pattern = Pattern(row, column, empty, blocked)
                self.patterns_for_cell[row, column].append(pattern)
                for cell in empty:
                    self.patterns_for_empty_cell[cell].append(pattern)
                for cell in blocked:
                    self.patterns_for_blocked_cell[cell].append(pattern)

        # empty number cells
        for cell in self.numbers:
            self._set(cell, False)

        # blocked border cells
        for row in range(self.height):
            self._set((row, -1), True)
            self._set((row, self.width), True)
        for column in range(self.width):
            self._set((-1, column), True)
            self._set((self.height, column), True)

    def _set(self, cell, blocked, because=None):
        if because is not None:
            print(cell, "is", blocked, "because", because)

        if blocked:
            matching_cells = self.blocked_cells
            matching_patterns = self.patterns_for_blocked_cell
            mismatching_patterns = self.patterns_for_empty_cell
        else:
            matching_cells = self.empty_cells
            matching_patterns = self.patterns_for_empty_cell
            mismatching_patterns = self.patterns_for_blocked_cell

        assert cell not in self.empty_cells
        assert cell not in self.blocked_cells
        self.unknown_cells.discard(cell)
        matching_cells.add(cell)
        updated = set()
        for pattern in mismatching_patterns[cell]:
            updated.add(pattern.cell)
            pattern.eliminated = True
        for pattern in matching_patterns[cell]:
            del pattern.blocked_cells[cell]

        return updated

    def all_number_cells(self):
        return self.patterns_for_cell.keys()

    def dump(self):
        data = ""
        for row in range(self.height):
            for column in range(self.width):
                cell = row, column
                if cell in self.numbers:
                    data += "{:02}".format(self.numbers[cell])
                elif cell in self.unknown_cells:
                    data += ".."
                elif cell in self.empty_cells:
                    data += "  "
                elif cell in self.blocked_cells:
                    data += "XX"
                else:
                    assert False
            data += "\n"
        return data


    def set(self, cell, blocked, because):
        updated = set()
        updated.update(self._set(cell, blocked, because))

        if blocked:
            row, col = cell
            for r, c in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                if 0 <= r < self.height and 0 <= c < self.width and (r, c) not in self.empty_cells:
                    updated.update(self._set((r, c), False, cell))

        return updated
if __name__ == "__main__":
    assert parse(example) == (9, 6, {(0, 2): 14, (1, 0): 8, (2, 5): 4, (4, 1): 2, (4, 4): 10, (6, 0): 4, (7, 5): 7, (8, 3): 7})
    assert cross(10, 20, 1) == [(set(), {(9, 20), (10, 21), (11, 20), (10, 19)})]
    assert cross(10, 20, 2) == [
        ({(10, 19)}, {(9, 20), (10, 21), (11, 20), (10, 18)}),
        ({(11, 20)}, {(9, 20), (10, 21), (12, 20), (10, 19)}),
        ({(10, 21)}, {(9, 20), (10, 22), (11, 20), (10, 19)}),
        ({(9, 20)}, {(8, 20), (10, 21), (11, 20), (10, 19)}),
    ]
    assert cross(10, 20, 3) == [
        ({(10, 19), (10, 18)}, {(9, 20), (10, 21), (11, 20), (10, 17)}),
        ({(11, 20), (10, 19)}, {(9, 20), (10, 21), (12, 20), (10, 18)}),
        ({(11, 20), (12, 20)}, {(9, 20), (10, 21), (13, 20), (10, 19)}),
        ({(10, 21), (10, 19)}, {(9, 20), (10, 22), (11, 20), (10, 18)}),
        ({(10, 21), (11, 20)}, {(9, 20), (10, 22), (12, 20), (10, 19)}),
        ({(10, 21), (10, 22)}, {(9, 20), (10, 23), (11, 20), (10, 19)}),
        ({(9, 20), (10, 19)}, {(8, 20), (10, 21), (11, 20), (10, 18)}),
        ({(9, 20), (11, 20)}, {(8, 20), (10, 21), (12, 20), (10, 19)}),
        ({(9, 20), (10, 21)}, {(8, 20), (10, 22), (11, 20), (10, 19)}),
        ({(9, 20), (8, 20)}, {(7, 20), (10, 21), (11, 20), (10, 19)}),
    ]
    assert State(example).dump().strip() == example.strip()
