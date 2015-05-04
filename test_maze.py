import unittest
import maze



class TestCell(unittest.TestCase):

    def setUp(self):
        self.matrix = maze.Matrix((6, 8))
        self.cell = maze.Cell((4, 5), self.matrix)

    def test_equality(self):
        cell1 = maze.Cell((1, 1), self.matrix)
        cell2 = maze.Cell((1, 1), self.matrix)
        self.assertEqual(cell1, cell2)

    def test_behaves_properly_with_sets(self):
        cell1 = maze.Cell((1, 1), self.matrix)
        cell2 = maze.Cell((1, 1), self.matrix)
        set1 = {cell1, cell2, cell1, cell2}
        set2 = {cell1, cell2}
        self.assertEqual(set1, set2)

    def test_in_boundary(self):
        self.assertTrue(
            self.cell.in_boundary((self.cell.pos), (self.cell.matrix_size))
        )

    def test_not_in_boundary(self):
        self.assertFalse(
            self.cell.in_boundary((6, 8), (self.cell.matrix_size))
        )

    def test_complete_neighbours(self):
        neigh_pos = [(3, 5), (4, 4), (5, 5), (4, 6)]
        neighbours = [maze.Cell(pos, self.matrix) for pos in neigh_pos]
        for neigh in neighbours:
            self.assertIn(neigh, self.cell.neighbours)

    def test_edge_cell_neighbours(self):
        cell = maze.Cell((5, 7), self.matrix)
        self.assertTrue(len(cell.neighbours) == 2)

    def test_append_wall_after(self):
        neighbour = maze.Cell((5, 5), self.matrix)
        neighbour.append_wall(self.cell)


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = maze.Matrix((6, 8))

    def test_populate_cells(self):
        self.matrix.populate_cells()
        self.assertEqual(len(self.matrix.cells), 6*8)

    def test_matrix_correct_row(self):
        row_no = len(self.matrix.matrix)
        self.assertEqual(row_no, 6)

    def test_matrix_correct_col(self):
        col_no = len(self.matrix.matrix[0])
        self.assertEqual(col_no, 8)

    def test_get_cell(self):
        cell1 = self.matrix.get_cell((4, 3))
        cell2 = maze.Cell((4, 3), self.matrix)
        self.assertEqual(cell1, cell2)

    def test_make_walls(self):
        self.matrix.make_walls()
        cell = self.matrix.get_cell((4, 5))
        walls = cell.walls
        self.assertTrue(len(walls) > 6)

    def test_get_wall(self):
        self.matrix.make_walls()
        cell1 = self.matrix.get_cell((4, 5))
        cell2 = self.matrix.get_cell((5, 5))
        cell_set = {cell1.pos, cell2.pos}
        wall = self.matrix.get_wall(cell_set)
        self.assertIsInstance(wall, maze.Wall)

if __name__ == '__main__':
    unittest.main()
