import unittest

from solver import Solver

class TestSolver(unittest.TestCase):
    def test_has_solution(self):
        self.assertTrue(Solver([1, 2, 3, 4]).has_solution())
        self.assertTrue(Solver([5, 5, 5, 1]).has_solution())
        self.assertTrue(Solver([7, 7, 3, 1]).has_solution())
        self.assertTrue(Solver([8, 8, 3, 3]).has_solution())
        self.assertFalse(Solver([1, 1, 1, 1]).has_solution())

if __name__ == '__main__':
    unittest.main()