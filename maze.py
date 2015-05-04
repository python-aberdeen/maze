"""
Maze Generator using Recursive Backtracker
"""
import random
import sys 


OFFSETS = ( 
    (0, -1),
    (0, 1), 
    (-1, 0), 
    (1, 0), 
)


class Cell:
    """ 
    Implementation of the cell. Able to add to a shared pool of walls,
    is aware of its neighbours, carries a visited marker and is aware
    of the size of the matrix in which it exists.
    It overloads the equality magic methods to ease comparison and to
    behave properly within sets - if needed.
    """
    walls = []

    def __init__(self, pos, matrix):
        self.pos = pos 
        self.row = pos[0]
        self.col = pos[1]
        self.matrix_size = matrix.size
        self.visited = False
        self.matrix = matrix

    @staticmethod
    def in_boundary(pos, size):
        "Check that pos is within matrix given matrix size"

        rows, cols = size
        return (
            pos[0] < rows
            and pos[1] < cols
            and pos[0] >= 0
            and pos[1] >= 0
        )   

    def append_wall(self, neighbour):
        "Create wall between neighbour if wall does not exist"
    
        wall = Wall(closed=True, cells={self.pos, neighbour.pos})
        if not wall in self.walls:
            self.walls.append(wall)

    def cell_walls(self):
        "Create cell's walls"

        for neigh in self.neighbours:
            self.append_wall(neigh)

    @property
    def neighbours(self):
        """
        Find all the valid neighbours and create necessary walls.
        """
        neighbours = []
        for offset in OFFSETS:
            row_off, col_off = offset
            neigh_pos = (self.row + row_off, self.col + col_off)
            if self.in_boundary(neigh_pos, self.matrix_size):
                neighbours.append(self.matrix.get_cell(neigh_pos))
        return neighbours

    def __eq__(self, other):
        """
        Override the default equals behavior
        to allow comparisons within a matrix or elsewhere
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """
        Define a non-equality test
        """
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """
        Override the default hash behavior
        (that returns the id or the object). This allows set
        operations
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        row, col = self.pos
        return "{}<{} {}>".format("cell", row, col)

    def __repr__(self):
        row, col = self.pos
        return "{}<{} {}>".format("cell", row, col)

class Wall:
    """
    Representing four sides of a cell
    """
    def __init__(self, closed=True, cells={None, None}):
        self.closed = closed
        self.cells = cells

    def __eq__(self, other):
        """
        Override the default Equals behavior by putting the cells of
        the walls being compared in a set to make the wall 'index agnostic'
        """
        if isinstance(other, self.__class__):
            return set(self.cells) == set(other.cells)
        return NotImplemented

    def __ne__(self, other):
        """
        Define a non-equality test
        """
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __str__(self):
        pos1, pos2 = self.cells
        closed = "closed" if self.closed else "open"
        return "{}<>{}:{}".format(pos1, pos2, closed)


class Matrix:
    """
    Implementation of the matrix class. The class populates its member cells
    and runs the backtracker.
    """

    # ToDo: Attack reduncies

    def __init__(self, size):
        self.size = size
        self.cells = {}

    @property
    def matrix(self):
        """
        Return the member cells in their positions.
        """
        # ToDo: Refactor Candidate
        return [
            [Cell((row, col), self) for col in range(self.size[1])]
            for row in range(self.size[0])
        ]

    def populate_cells(self):
        """
        Populate the cells in the matrix the cells attribute is a list of
        dictionaries which has tuples as keys and a set of tuples representing position
        as values
        """

        for row in self.matrix:
            for cell in row:
                self.cells.update({cell.pos: cell})

    def get_cell(self, pos):
        "Return a cell given the position of the cell"

        if not self.cells:
            self.populate_cells()
        return self.cells[pos]

    def make_walls(self):
        "Create all walls"
    
        for row in self.matrix:
            for cell in row:
                cell.cell_walls()
        return True

    def get_wall(self, duo):
        """
        Gets the wall between two cells. 
        Position of cells are passed as a set of tuples"""
        cell = self.get_cell((0, 0))
        walls = cell.walls
        wall = [wall for wall in walls if wall.cells == duo]
        return wall[0] if wall else None

    def unvisited_exist(self):
        for dummy, cell in self.cells.items():
            if not cell.visited:
                return cell
        return False

    def run_matrix(self, initial_cell):
        """
        Depth-first search by recursive backtracker
        http://en.wikipedia.org/wiki/Maze_generation_algorithm
        """
        stack = []
        unvisited = dict(self.cells)
        current_cell = initial_cell
        while self.unvisited_exist():
            current_cell.visited = True
            try:
                del unvisited[current_cell.pos]
            except KeyError:
                pass
            neighbours = current_cell.neighbours
            unvisited_neighs = [
                cell for cell in neighbours if not cell.visited
            ]
            if unvisited_neighs:
                stack.append(current_cell)
                stale_cell = current_cell
                current_cell = random.choice(unvisited_neighs)
                duo = set([stale_cell.pos, current_cell.pos])
                shared_wall = self.get_wall(duo)
                shared_wall.closed = False
            elif stack:
                current_cell = stack.pop()
            else:
                cell_rep = random.choice(unvisited)
                _, current_cell = cell_rep.items()
