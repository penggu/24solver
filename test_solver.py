import unittest

from solver import Solver

class TestSolver(unittest.TestCase):
    def test_solve_24(self):
        self.assertGreater(len(Solver([1, 2, 3, 4]).solve()), 0)
        self.assertGreater(len(Solver([5, 5, 5, 1]).solve()), 0)
        self.assertGreater(len(Solver([7, 7, 3, 1]).solve()), 0)
        self.assertGreater(len(Solver([8, 8, 3, 3]).solve()), 0)
        self.assertEqual(len(Solver([1, 1, 1, 1]).solve()), 0)

if __name__ == '__main__':
    unittest.main()